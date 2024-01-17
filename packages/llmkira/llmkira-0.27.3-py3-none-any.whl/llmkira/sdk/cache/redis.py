# -*- coding: utf-8 -*-
# @Time    : 2023/7/10 下午9:43
# @Author  : sudoskys
# @File    : redis.py
# @Software: PyCharm
import json
from typing import Optional, Tuple, List, Union

import redis
from loguru import logger
from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool

from .base import AbstractDataClass, PREFIX


class RedisClientWrapper(AbstractDataClass):
    """
    Redis 数据类
    """

    def __init__(self, backend, prefix=PREFIX):
        self.prefix = prefix
        self.connection_pool = redis.asyncio.ConnectionPool.from_url(backend)
        self._redis = redis.asyncio.Redis(connection_pool=self.connection_pool)

    async def ping(self):
        return await self._redis.ping()

    def update_backend(self, backend):
        self.connection_pool = ConnectionPool.from_url(backend)
        self._redis = Redis(connection_pool=self.connection_pool)
        return True

    async def set_data(self, key, value, timeout=None):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        return await self._redis.set(
            name=f"{self.prefix}{key}", value=value, ex=timeout
        )

    async def read_data(self, key) -> Optional[Union[str, dict, int]]:
        data = await self._redis.get(self.prefix + str(key))
        if data is not None:
            try:
                data = json.loads(data)
            except Exception as ex:
                logger.trace(ex)
                pass
        return data

    async def lpush_data(self, key, value):
        """
        从左侧插入数据
        :param key: str
        :param value: json
        """
        # 验证是否可以被json序列化
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        return await self._redis.lpush(self.prefix + str(key), value)

    async def lpop_data(self, key) -> Optional[dict]:
        _data = await self._redis.lpop(self.prefix + str(key))
        if _data:
            _data = _data.decode("utf-8")
            try:
                _data = json.loads(_data)
            except json.JSONDecodeError:
                pass
            return _data
        return None

    async def lrange_data(self, key, start_end: Tuple[int, int] = (0, -1)) -> List[str]:
        _items = await self._redis.lrange(
            self.prefix + str(key), start=start_end[0], end=start_end[1]
        )
        items = [m.decode("utf-8") for m in _items[::-1]]
        return items
