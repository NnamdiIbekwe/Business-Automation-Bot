


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

context = {**flatten(event.payload), "event.type": event.type, "event.id": str(event.id)}
    matched = failed = 0
    for workflow in workflows:
        if not matches(workflow.condition, event.payload):
            continue
        matched += 1
        results, ok = [], True
        for action in workflow.actions:
            result = run_action(action, context)
            results.append(result)
            if not result["ok"]:
                ok = False
                break
        failed += 0 if ok else 1
        db.add(Run(workflow_id=workflow_id, event_id=event_id,
                    status="success" if ok else "failed", detail=results))
    
    event.status = "ignored" if matched == 0 else ("failed" if failed else "processed")
    db.commit()