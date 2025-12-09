from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.backend.middleware.logginMidd import Log
from app.backend.routes import sensor_routes
from test.scheduler_test import start_test
from fastapi.staticfiles import StaticFiles

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        start_test()
        print("Scheduler avviato.")
    except Exception as e:
        print("Errore avvio scheduler:", e)

    yield
    print("Server in spegnimento...")

app = FastAPI(title="SmartMeter",lifespan=lifespan)

app.add_middleware(Log)
app.include_router(sensor_routes.router)

app.mount("/", StaticFiles(directory="app/frontend", html=True), name="frontend")

# uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)