


MISSING = object()

OPERATORS = {
    "eq": lambda a, b: a == b,
    "contains": lambda a, b: b in a,   
}

def get_path(data, path):
    current = data
    for part in path.split("."):
        if isinstance(current, dict) and part in current:
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

def process_event(event_id: int) -> None:
    with SessionLocal() as db:
        event = db.get(Event, event_id)
        if event is None:
            logger.warning("event %s not found", event_id)
            return
        
        workflows = db.scalar(
            select(workflow).where(workflow.enabled.is_(True), workflow.event_type == event.type)
        ).all()