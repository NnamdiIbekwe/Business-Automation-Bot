


MISSING = object()

OPERATORS = {
    "eq": lambda a, b: a == b,
    "contains": lambda a, b: b in a,   
}

def get_path(data, path):
    current = data
    for part in path.split("."):
        if isinstance(current, dict) and path in current:
            current = current[part]
        else:
            return MISSING
    return current

def matches(condition, payload):
    if not condition:
        return True
    actual = get_path(payload, condition["field"])
    if actual is MISSING:
        return False
    try:
        return bool(OPERATORS[condition["op"]](actual, condition["value"]))
    except TypeError:
        return False