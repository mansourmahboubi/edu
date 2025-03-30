"""
Creatioonal:
    Factory Method
        3 Component and Identifer
            1. Creator
            2. Product
            3. Client
Provides an interface for creating objects in a superclass,
    but allows subclasses to alter the type of objects that will be created.
"""

### THE Answer using factory method ###
from abc import ABC, abstractmethod


class Creator(ABC):
    @abstractmethod
    def make(self):
        pass

    def call_edit(self):
        product = self.make()
        result = product.edit()  # type: ignore
        return result


class JsonCreator(Creator):
    def make(self):
        return JSONProduct()


class XmlCreator(Creator):
    def make(self):
        return XMLProduct()


class Product(ABC):
    @abstractmethod
    def edit(self, file):
        pass


class JSONProduct(Product):
    def edit(self):
        return "editing json file ..."


class XMLProduct(Product):
    def edit(self):
        return "editing xml file ..."


def client(format):
    return format.call_edit()


print(client(JsonCreator()))
