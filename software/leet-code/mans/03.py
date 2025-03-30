"""
flatten a nested JSON object
"""


def key_name(name, key):
    return f"{key}_{name}" if key else name


def flat_object(obj):
    flat_dict = {}
    # nested_props = {}
    def flasten(value, key=None):
        if isinstance(value, dict):
            for key_1, value in value.items():
                flasten(value, key=key_name(key_1, key))
        elif isinstance(value, list):
            for idx, item in enumerate(value):
                flasten(item, key=key_name(idx, key))
        else:
            flat_dict[key] = value  # type:ignore

    flasten(obj)

    return flat_dict


if __name__ == "__main__":
    sample_dict = {
        "a": {
            "b": {
                "c": 5,
                "d": [
                    9,
                    {"t": 5},
                    8,
                    8,
                ],
            }
        },
        "d": {"e": {"f": 8}},
    }
    a = flat_object(sample_dict)
    print(a)
