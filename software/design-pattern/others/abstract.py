"""
    Abstract clas. Abstraact method
"""
from abc import ABC, abstractmethod


# Abstract class
class A(ABC):
    @abstractmethod
    def show(self):
        pass


class B(A):
    def show(self):
        pass


b1 = B()
