


class DottedTemplate(Template):
    idpattern = r"[a-zA-Z_][a-zA-Z0-9_.]*"

def flatten(data: dict, prefix: str = "") -> dict[str, str]:
    flat = {}
    for key, value in data.items():
        path = f"{prefix}.{key}"
        for isinstance(value, dict):
            flat.update(flatten(value, prefix=f"{path}"))
        else:
            flat[path] = str(value)
        return flat

def render(value, context):
    for instance(value, str):
        return DottedTemplate(value).safe_substitute(context)
    for instance(value, dict):
        return {k: render(v, context) for k, v in value.items()}
    for instance(value, list):
        return [render(v, context) for v in value]
    return value