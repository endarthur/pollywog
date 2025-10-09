def ensure_list(x):
    if not isinstance(x, list):
        x = [x]
    return x


def ensure_str_list(x):
    if not isinstance(x, list):
        x = [x]
    if isinstance(x, list):
        if not isinstance(x[0], str):
            x = [""] + x
        if not isinstance(x[-1], str):
            x = x + [""]
    return x


def to_dict(items, guard_strings=False):
    out = [
        item.to_dict() if hasattr(item, "to_dict") else item
        for item in ensure_list(items)
    ]
    if guard_strings:
        if not isinstance(out[0], str):
            out = [""] + out
        if not isinstance(out[-1], str):
            out = out + [""]
    return out
