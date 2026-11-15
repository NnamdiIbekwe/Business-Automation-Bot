


def _emit_tick() -> None:
    with SessionLocal() as db:
        event = Event(type="schedule.tick", payload={"at": datetime.now(timezone.utc).isoformat()})
        db.add(event)
        db.commit()
        event_id = event.id
    process_event(event_id)

async def ticker(interval_seconds: int) -> None:
    while True:
        await asyncio.sleep(interval_seconds)
        await asyncio.to_thread(_emit_tick)