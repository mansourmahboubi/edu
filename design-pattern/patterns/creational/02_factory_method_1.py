"""
    Creatioonal:
        Factory Method
            3 Component and Identifer
                1. Creator
                2. Product
                3. Client

    Factory Method is a creational design pattern 
    that provides an interface for creating objects in a superclass,
    but allows subclasses to alter the type of objects that will be created.

    https://refactoring.guru/design-patterns/factory-method

    Objects returned by a factory method are often referred to as products.
"""

### THE PROBLEM ###
# class A:
#     def __init__(self, name: str, format: str) -> None:
#         self.name = name
#         self.format = format


# class B:
#     def edit(self, file):
#         if file.format == "json":
#             print(f"editing json file ... {file.name}")
#         elif file.format == "xml":
#             print(f"editing xml file ... {file.name}")
#         else:
#             raise ValueError(f"{file.format} is not supported")


# a1 = A("first", "json")
# b1 = B()
# b1.edit(a1)

### THE Answer ###


class A:
    def __init__(self, name: str, format: str) -> None:
        self.name = name
        self.format = format


class B:
    def edit(self, file):  # client
        edit = self._get_edit(file)
        return edit(file)

    def _get_edit(self, file):  # creator
        if file.format == "json":  # identifier
            return self.json_edit
        elif file.format == "xml":  # identifier
            return self.xml_edit
        else:
            raise ValueError(f"{file.format} is not supported")

    def json_edit(self, file):  # product
        print(f"editing json file ... {file.name}")

    def xml_edit(self, file):  # product
        print(f"editing xml file ... {file.name}")


a1 = A("first", "json")
b1 = B()
b1.edit(a1)
