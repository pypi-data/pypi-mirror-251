# -*- coding: utf-8 -*-
# @Time    : 2023/9/18 下午10:26
# @Author  : sudoskys
# @File    : __init__.py.py
# @Software: PyCharm
import json
import re
from copy import deepcopy
from typing import Optional, Dict, Union, List

from llmkira.sdk.cache import global_cache_runtime


class EnvManager(object):

    def __init__(self, uid: Optional[str] = None):
        self.uid = uid

    @staticmethod
    def parse_env(env_string) -> Dict[str, str]:
        if not env_string.endswith(";"):
            env_string = env_string + ";"
        pattern = r'(\w+)\s*=\s*(.*?)\s*;'
        matches = re.findall(pattern, env_string, re.MULTILINE)
        _env_table = {}
        for match in matches:
            _key = match[0]
            _value = match[1]
            _value = _value.strip().strip("\"")
            _key = _key.upper()
            _env_table[_key] = _value
        return _env_table

    @classmethod
    def _prefix(cls, uid: str) -> str:
        return f"env:{uid}"

    @classmethod
    def from_uid(cls, uid: str) -> "EnvManager":
        _c = cls()
        _c.uid = uid
        return _c

    @classmethod
    def from_meta(cls, platform: str, user_id: Union[str, int]) -> "EnvManager":
        _c = cls()
        _c.uid = f"{platform}:{user_id}"
        return _c

    async def __get_env(self) -> dict:
        cache = global_cache_runtime.get_redis()
        _cache = await cache.read_data(key=self._prefix(uid=self.uid))
        if not isinstance(_cache, dict):
            return {}
        return _cache

    async def get_env(self, name: str) -> Optional[dict]:
        """
        获取用户环境变量
        :param name: 环境变量名
        :return: 环境变量
        """
        _cache = await self.__get_env()
        return _cache.get(name.upper(), None)

    async def get_env_list(self, name_list: List[str]) -> dict:
        _cache = await self.__get_env()
        _env = {}
        for name in name_list:
            _env[name] = _cache.get(name.upper(), None)
        return _env

    async def update_env(self, env: Dict[str, str]) -> dict:
        """
        更新用户环境变量
        :param env: 环境变量
        :return: 更新后的环境变量
        """
        cache = global_cache_runtime.get_redis()
        _env = await self.__get_env()
        _user_env = deepcopy(_env)
        # 检查是否为一级嵌套
        for _key, _value in env.items():
            _key = str(_key).upper()
            _value = str(_value)
            if _value == "":
                _user_env.pop(_key, None)
                continue
            _user_env[_key] = _value
        _cache = await cache.set_data(key=self._prefix(uid=self.uid),
                                      value=json.dumps(_user_env),
                                      timeout=60 * 60 * 24 * 7)
        return _user_env
