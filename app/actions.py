


logger = logging.getlogger("bot.actions")


def _log(params: dict, context: dict) -> dict[str, Any]:
    message = render(params.get("message", "workflow fired"), context)
    logger.info("ACTION log: %s", message)
    return {"message": message}