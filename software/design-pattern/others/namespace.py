"""
Namespaces
    built-in namespace
        Global namespace
            Enclosed namespace
                Local namespace
   global(), local()
   global, non-local
"""

print(dir(__builtins__))


def outer():
    # enclosed namespace
    x: int = 2  # noqa: F841

    def inner():
        # local namespace
        x = 1  # noqa: F841
