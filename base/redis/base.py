from typing import Union


class BaseRedis:
    def get(self, *args, **kwargs):
        raise NotImplementedError(f"Define get() method in {self.__class__.__name__}")

    def put(self, *args, **kwargs):
        raise NotImplementedError(f"Define put() method in {self.__class__.__name__}")
