


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