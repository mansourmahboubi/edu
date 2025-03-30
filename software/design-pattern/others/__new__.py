"""
    __new__
"""

class A:
    def __init__(self, name) -> None:
        # second init gets called
        self.name = name
    
    def __new__(cls, name,*args, **kwargs):
        # first new gets called
        if(name =="john"):
            return None
        else:
            return super().__new__(cls, *args, **kwargs)

a1 =A("john")

print(a1)
# return type
print(a1.__class__.__class__)