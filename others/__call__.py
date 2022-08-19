"""
    __call__() method is called when the instance is called.
"""


class A:
    def __call__(self, *args, **kwargs):
        print("I am called")


a = A()
a()
