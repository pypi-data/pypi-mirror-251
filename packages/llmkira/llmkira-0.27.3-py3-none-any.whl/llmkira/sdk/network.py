import asyncio
import atexit
import json
from typing import Any

import httpx
from loguru import logger

from .error import RateLimitError, ServiceUnavailableError, AuthenticationError, CheckError

__session_pool = {}


def llm_error_handler(code, message: str):
    if code == 429:
        raise RateLimitError(message)
    elif code == 404 and not message:
        raise ServiceUnavailableError(f"invalid endpoint, {message}")
    elif code == 500 or code != 401:
        raise ServiceUnavailableError(message)
    else:
        raise AuthenticationError(message)


def check_json_response(status_code: int, req_data: dict):
    """
    检查json响应
    """
    if req_data.get("object", None) == "error":
        raise CheckError(
            f"[CODE]{status_code}:{req_data.get('code', 404)}"
        )
    # 错误消息
    if req_data.get("error", None):
        _error = req_data.get("error", "your endpoint is not a valid endpoint, please check it")
        if status_code == 404:
            raise CheckError(
                f"[Invalid endpoint] {_error}, do you forget to add something like v1/chat/completions?"
            )
        raise CheckError(
            f"{status_code}:{_error.get('type')}:{_error.get('message')}"
        )
    # 错误消息
    if isinstance(req_data.get("message"), str):
        raise CheckError(
            f"{status_code}:{req_data.get('message')}"
        )
    if status_code == 404:
        raise CheckError(
            f"[Invalid endpoint] no error message return...  do you forget to add something like v1/chat/completions?"
        )


async def request(
        method: str,
        url: str,
        params: dict = None,
        data: Any = None,
        headers: dict = None,
        json_body: bool = False,
        proxy: str = "",
        call_func=None,
        timeout: int = 300,
        **kwargs,
):
    """
    请求
    :param call_func: 错误回调函数
    :param method:
    :param url:
    :param params:
    :param data:
    :param headers:
    :param json_body:
    :param proxy:
    :param timeout:
    :param kwargs: 参数
    :return:
    """
    if headers is None:
        headers = {}
    if params is None:
        params = {}
    config = {
        "method": method.upper(),
        "url": url,
        "params": params,
        "data": data,
        "headers": headers,
    }
    # 更新
    config.update(kwargs)
    if json_body:
        config["headers"]["Content-Type"] = "application/json"
        config["data"] = json.dumps(config["data"]).encode()
    # SSL
    # config["ssl"] = False

    # timeout
    config["timeout"] = timeout

    # 请求
    session = get_session(proxy=proxy)
    resp = await session.request(**config)

    # 检查响应头 Content-Length
    content_length = resp.headers.get("content-length")
    if content_length and int(content_length) == 0:
        return None

    # 检查响应头 Content-Type
    content_type = resp.headers.get("content-type")
    if content_type.lower().find("application/json") == -1:
        logger.error(f"[105232]Server send a invalid response {resp.text}")
        raise Exception("Server send a invalid response with content-type:{}".format(content_type))

    try:
        req_data: dict = json.loads(resp.text)
    except json.JSONDecodeError:
        if resp.status_code != 200:
            raise Exception(f"[Request {resp.status_code}] Request failed without any error message")
        raise Exception("Server send a invalid json response")

    try:
        check_json_response(resp.status_code, req_data)
    except CheckError as e:
        logger.error(e)
        # Message 格式校验失败
        if call_func:
            call_func(req_data, headers)
        _status = req_data.get("status", None)
        llm_error_handler(
            code=_status,
            message=f"{resp.status_code}:{req_data.get('message')}"
        )
    except Exception as e:
        raise e
    return req_data


def get_session(proxy: str = ""):
    global __session_pool
    loop = asyncio.get_event_loop()
    session = __session_pool.get(loop, None)
    if session is None:
        if proxy:
            proxies = {"all://": proxy}
            session = httpx.AsyncClient(timeout=300, proxies=proxies)
        else:
            session = httpx.AsyncClient(timeout=300)
        __session_pool[loop] = session
    return session


@atexit.register
def __clean():
    """
    程序退出清理操作。
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        return

    async def __clean_task():
        await __session_pool[loop].close()

    if loop.is_closed():
        loop.run_until_complete(__clean_task())
    else:
        loop.create_task(__clean_task())
