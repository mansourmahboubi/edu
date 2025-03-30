"""
products
books -> Edu, History, Biology
"""

from abc import ABC, abstractmethod
from typing import List


class BaseCreator(ABC):
    @abstractmethod
    def factory_method(self) -> "BaseBook":
        pass

    def process(self):
        product = self.factory_method()
        excerpt = product.excerpt()
        return excerpt


class HistoryBookCreator(BaseCreator):
    def factory_method(self):
        return HistoryBook()


class EduBookCreator(BaseCreator):
    def factory_method(self):
        return EduBook()


class BaseBook(ABC):
    """
    Concrete products
    """

    @abstractmethod
    def excerpt(self) -> "List[str]":
        pass


class HistoryBook(BaseBook):
    def excerpt(self):
        return ["Boosh", "Merkel", "Ajmadinejad"]


class EduBook(BaseBook):
    def excerpt(self):
        return ["Learn", "How", "Why"]


class BiologyBook(BaseBook):
    def excerpt(self):
        return ["Human", "Body", "Blood"]


def client(creator: "BaseCreator"):
    print(creator.process())


if __name__ == "__main__":
    creator = HistoryBookCreator()
    client(creator)

    creator_2 = EduBookCreator()
    client(creator_2)
