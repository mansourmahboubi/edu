"""
flatten a nested JSON object
"""


def flat_object(obj):
    flat_dict = {}
    # nested_props = {}
    def flasten(value, key):
        if isinstance(value, dict):
            for key_1, value in value.items():
                flasten(value, key=f"{key}_{key_1}")
        elif isinstance(value, list):
            for item in value:
                flasten(item, key=f"{key}_{item}")
        else:
            flat_dict[key] = value  # type:ignore

    for key, value in obj.items():
        flasten(value, key=key)

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
