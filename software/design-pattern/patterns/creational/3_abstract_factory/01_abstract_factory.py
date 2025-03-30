"""
Creational patterns: Abstract Factory
    Car => Benz, Bmw => Suv, Coupe
        benz suv => gla, glc
        bmw suv => x1, x2

        benz coupe => cls, E-class
        bmw coupe => m2, m4

lets you produce families of related objects
    without specifying their concrete classes.
"""

from abc import ABC, abstractmethod


class Car(ABC):
    @abstractmethod
    def call_suv(self):
        pass

    @abstractmethod
    def call_coupe(self):
        pass


# --------------------------------- division --------------------------------- #
class Benz(Car):
    def call_suv(self):
        return Gla()

    def call_coupe(self):
        return Cls()


class Bmw(Car):
    def call_suv(self):
        return X1()

    def call_coupe(self):
        return M2()


class Suv(ABC):
    @abstractmethod
    def creating_suv(self):
        pass


class Coupe(ABC):
    @abstractmethod
    def creating_coupe(self):
        pass


class Gla(Suv):
    def creating_suv(self):
        print((f"creating benz gla suv"))


class X1(Suv):
    def creating_suv(self):
        print((f"creating benz suv x1"))


class Cls(Coupe):
    def creating_coupe(self):
        print((f"creating benz cls coupe"))


class M2(Coupe):
    def creating_coupe(self):
        print((f"creating bmw m2 coupe"))


def client_suv(order):
    suv = order.call_suv()
    suv.creating_suv()


def client_coupe(order):
    coupe = order.call_coupe()
    coupe.creating_coupe()


if __name__ == "__main__":
    order = Bmw()
    client_coupe(order)

    benz_order = Benz()
    client_suv(benz_order)
    # client_suv(order)
    # client_coupe(order)
