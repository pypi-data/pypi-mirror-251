# -*- coding: utf-8 -*-
from pydantic import ConfigDict

__package__name__ = "llmkira.extra.plugins.search"
__plugin_name__ = "search_in_google"
__openapi_version__ = "20231111"

from llmkira.extra.user import CostControl, UserCost
from llmkira.middleware.llm_provider import GetAuthDriver
from llmkira.sdk import resign_plugin_executor
from llmkira.sdk.endpoint import openai
from llmkira.sdk.func_calling import verify_openapi_version

verify_openapi_version(__package__name__, __openapi_version__)
from loguru import logger  # noqa: E402
from pydantic import BaseModel  # noqa: E402

from llmkira.schema import RawMessage  # noqa: E402
from llmkira.sdk.func_calling import BaseTool, PluginMetadata  # noqa: E402
from llmkira.sdk.func_calling.schema import FuncPair  # noqa: E402
from llmkira.sdk.schema import create_short_task, Function  # noqa: E402
from llmkira.task import Task, TaskHeader  # noqa: E402
from typing import TYPE_CHECKING  # noqa: E402

if TYPE_CHECKING:
    from llmkira.sdk.schema import TaskBatch
search = Function(
    name=__plugin_name__,
    description="Search/validate on google.com.[ONLY IF NECESSARY]",
).update_config(
    config=Function.FunctionExtra(
        system_prompt="Search only if necessary",
    )
)
search.add_property(
    property_name="keywords",
    property_description="question entered in the search website",
    property_type="string",
    required=True,
)


@resign_plugin_executor(function=search)
def search_on_duckduckgo(search_sentence: str, key_words: str = None):
    logger.debug(f"Plugin --search_on_duckduckgo {search_sentence}")
    from duckduckgo_search import DDGS

    # 内存优化抛弃 NLP
    # from llmkira.sdk.filter import Sublimate
    sort_text = []
    link_refer = {}
    with DDGS(timeout=20) as ddgs:
        search_result = ddgs.text(search_sentence)
        for r in search_result:
            _title = r.get("title")
            _href = r.get("href")
            _body = r.get("body")
            link_refer[_body] = _href
            sort_text.append((_body, _title, _href))
    # must_key = [key_words] if key_words else None
    sorted_result = sort_text
    # sorted_result = Sublimate(sort_text).valuation(match_sentence=search_sentence, match_keywords=must_key)
    valuable_result = [item[0] for item in sorted_result[:4]]
    # 构建单条内容
    clues = []
    for key, item in enumerate(valuable_result):
        clues.append(
            f"\nPage #{key}\n🔍Contents:{item}\n"
            f"🔗Source:{link_refer.get(item, 'https://google.com/')}\n"
        )
    content = "\n".join(clues)
    return (
        "[🔍SearchPage]\n"
        + content
        + (
            "\n[Page End]"
            "\n[ReplyFormat:`$summary_answer \n [$index]($source_link) * num` to mark links]"
        )
    )


class Search(BaseModel):
    keywords: str
    model_config = ConfigDict(extra="allow")


class SearchTool(BaseTool):
    """
    搜索工具
    """

    silent: bool = False
    function: Function = search
    keywords: list = [
        "怎么",
        "How",
        "件事",
        "牢大",
        "作用",
        "知道",
        "什么",
        "认识",
        "What",
        "http",
        "what",
        "who",
        "how",
        "Who",
        "Why",
        "作品",
        "why",
        "Where",
        "了解",
        "简述",
        "How to",
        "是谁",
        "how to",
        "解释",
        "怎样的",
        "新闻",
        "ニュース",
        "电影",
        "番剧",
        "アニメ",
        "2022",
        "2023",
        "请教",
        "介绍",
        "怎样",
        "吗",
        "么",
        "？",
        "?",
        "呢",
        "评价",
        "搜索",
        "百度",
        "谷歌",
        "bing",
        "谁是",
        "上网",
    ]

    def pre_check(self):
        try:
            from duckduckgo_search import DDGS  # noqa: F401

            # from llmkira.sdk.filter import Sublimate
            return True
        except ImportError as e:
            logger.warning(
                f"plugin:package <duckduckgo_search> not found,please install it first:{e}"
            )
            return False

    def func_message(self, message_text, **kwargs):
        """
        如果合格则返回message，否则返回None，表示不处理
        """
        for i in self.keywords:
            if i in message_text:
                return self.function
        # 正则匹配
        if self.pattern:
            match = self.pattern.match(message_text)
            if match:
                return self.function
        return None

    async def failed(
        self,
        task: "TaskHeader",
        receiver: "TaskHeader.Location",
        exception,
        env: dict,
        arg: dict,
        pending_task: "TaskBatch",
        refer_llm_result: dict = None,
        **kwargs,
    ):
        _meta = task.task_meta.reply_notify(
            plugin_name=__plugin_name__,
            callback=[
                TaskHeader.Meta.Callback.create(
                    name=__plugin_name__,
                    function_response=f"Run Failed {exception}",
                    tool_call_id=pending_task.get_batch_id(),
                )
            ],
            write_back=True,
            release_chain=True,
        )
        await Task(queue=receiver.platform).send_task(
            task=TaskHeader(
                sender=task.sender,
                receiver=receiver,
                task_meta=_meta,
                message=[
                    RawMessage(
                        user_id=receiver.user_id,
                        chat_id=receiver.chat_id,
                        text=f"🍖{__plugin_name__} Run Failed：{exception}",
                    )
                ],
            )
        )

    @staticmethod
    async def llm_task(plugin_name, task: TaskHeader, task_desc: str, raw_data: str):
        assert task_desc == raw_data, "STOP USE THE FUNCTION"
        # TODO: 转换为通用
        logger.info("llm_tool:{}".format(task_desc))
        auth_client = GetAuthDriver(uid=task.sender.uid)
        driver = await auth_client.get()
        endpoint = openai.Openai.init(
            driver=driver,
            temperature=0.1,
            messages=create_short_task(task_desc=task_desc, refer=raw_data),
        )
        # 调用Openai
        result = await endpoint.create()
        # 记录消耗
        await CostControl.add_cost(
            cost=UserCost.create_from_function(
                uid=task.sender.uid,
                request_id=result.id,
                cost_by=plugin_name,
                token_usage=result.usage.total_tokens,
                token_uuid=driver.uuid,
                model_name=driver.model,
            )
        )
        assert result.default_message.content, "llm_task.py:llm_task:content is None"
        return result.default_message.content

    async def callback(
        self,
        task: "TaskHeader",
        receiver: "TaskHeader.Location",
        env: dict,
        arg: dict,
        pending_task: "TaskBatch",
        refer_llm_result: dict = None,
        **kwargs,
    ):
        return True

    async def run(
        self,
        task: "TaskHeader",
        receiver: "TaskHeader.Location",
        arg: dict,
        env: dict,
        pending_task: "TaskBatch",
        refer_llm_result: dict = None,
    ):
        """
        处理message，返回message
        """

        _set = Search.model_validate(arg)
        _search_result = search_on_duckduckgo(_set.keywords)
        # META
        _meta = task.task_meta.reply_raw(
            plugin_name=__plugin_name__,
            callback=[
                TaskHeader.Meta.Callback.create(
                    name=__plugin_name__,
                    function_response=str(_search_result),
                    tool_call_id=pending_task.get_batch_id(),
                )
            ],
        )
        await Task(queue=receiver.platform).send_task(
            task=TaskHeader(
                sender=task.sender,  # 继承发送者
                receiver=receiver,  # 因为可能有转发，所以可以单配
                task_meta=_meta,
                message=[
                    RawMessage(
                        user_id=receiver.user_id,
                        chat_id=receiver.chat_id,
                        text="🔍 Searching Done",
                    )
                ],
            )
        )


__plugin_meta__ = PluginMetadata(
    name=__plugin_name__,
    description="Search fact on google.com",
    usage="以问号结尾的句子即可触发",
    openapi_version=__openapi_version__,
    function={FuncPair(function=search, tool=SearchTool)},
)
