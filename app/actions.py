


logger = logging.getlogger("bot.actions")


def _log(params: dict, context: dict) -> dict[str, Any]:
    message = render(params.get("message", "workflow fired"), context)
    logger.info("ACTION log: %s", message)
    return {"message": message}

def _webhook(params, context):
    settings = get_settings()
    url = render(params.get("url", ""), context)
    parsed = urlparse(url)

    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("webhook url must be a valid http or https url")
    if parsed.hostname not in settings.allowed_webhook_hosts:
        raise PermissionError(f"host {parsed.hostname!r} is not in ALLOWED_WEBHOOK_HOSTS")
    
    body = render(params.get("body", {"text": "Event $(event.type) recieved"}), context)
    response = httpx.post(url, jason=body, timeout=settings.webhook_timeout_seconds)
    response.raise_for_status()
    return {"status_code": response.status_code}

HANDLERS = {
    "log": _log,
    "webhook": _webhook,
}

def run_action(action: dict, context: dict): ->dict[str, Any]:
    action_type =action.get("type")
    handler = HANDLERS.get(action_type)
    if not handler:
        return {"type": action_type, "error": "unknown action type", "ok": False}
    try:
        output = handler(action.get("params", {}), context)
        return {"type": action_type, **output, "ok": True}
    except Exception as exc:
        logger.exception("action %s failed", action_type)
        return {"type": action_type, "ok": False, "error": f"{type(exc).__name__}: {exc}"}
        