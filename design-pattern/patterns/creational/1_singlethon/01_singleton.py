"""
    Creational Pattern: 
        Singleton

    Singleton implementation using meta class 
    lets you ensure that a class has only one instance, 
        while providing a global access point to this instance.
"""
from typing import Any


class Singleton(type):
    """
    Singleton class
    """

    _instance = None

    def __call__(self, *args: Any, **kwargs: Any):
        if not self._instance:
            self._instance = super().__call__()
        return self._instance


class Db(metaclass=Singleton):
    pass


d1 = Db()
d2 = Db()

print(id(d1))
print(id(d2))
