


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
