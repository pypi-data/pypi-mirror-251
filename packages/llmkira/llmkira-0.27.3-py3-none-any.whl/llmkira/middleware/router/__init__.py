# -*- coding: utf-8 -*-
# @Time    : 2023/8/21 下午10:19
# @Author  : sudoskys
# @File    : __init__.py.py
# @Software: PyCharm
from typing import List, Union

from .schema import RouterCache, Router
from ...schema import singleton
from ...sdk.cache import global_cache_runtime
from ...sdk.utils import sync


@singleton
class RouterManager(object):
    def __init__(self):
        self.__redis_key__ = "router"
        self.router = sync(self._sync())

    async def _upload(self):
        cache = global_cache_runtime.get_redis()
        assert isinstance(self.router, RouterCache), "router info error"
        # self.router = RouterCache.model_validate(self.router.dict())
        return await cache.set_data(key=self.__redis_key__, value=self.router.model_dump_json())

    async def _sync(self) -> RouterCache:
        cache = global_cache_runtime.get_redis()
        _cache = await cache.read_data(key=self.__redis_key__)
        if not _cache:
            return RouterCache()
        try:
            sub_info = RouterCache().model_validate(_cache)
        except Exception:
            raise Exception(f"not found router info")
        return sub_info

    def get_router_by_user(self, to_: str, user_id: Union[str, int]) -> List[Router]:
        _all = self.router.router
        assert user_id, "user_id is None"
        user_id = str(user_id)
        return [router for router in _all if str(router.user_id) == str(user_id) and router.to_ == to_]

    def get_router_by_sender(self, from_: str) -> List[Router]:
        _all = self.router.router
        return [router for router in _all if router.from_ == from_]

    def add_router(self, router: Router) -> None:
        self.router.router.append(router)
        sync(self._upload())

    def remove_router(self, router: Router) -> None:
        if router in self.router.router:
            self.router.router.remove(router)
        sync(self._upload())
