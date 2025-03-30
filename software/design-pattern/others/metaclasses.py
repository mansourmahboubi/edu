"""
    Meta class
"""


class A:
    def __new__(cls, *args, **kwargs):
        # initiated by type meta class
        print(cls)
        return super().__new__(cls)


a1 = A()
# print(a1.__class__)
"""
# type is a meta class
a2 =  type("Person", (), {})
print(a2)
"""
