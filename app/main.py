from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}



@asynccontextmanager
async def lifespan(app: FastAPI):
    Beta.metadata.create_all(engine)
    task = None
    if settings.scheuler_interval_seconds > 0:
        task = asyncio.create_task(ticker(settings.scheduler_interval_seconds))
    yield
    if task:
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            awiat task