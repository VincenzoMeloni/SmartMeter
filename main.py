from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.backend.middleware.logginMidd import Log
from app.backend.routes import sensor_routes
from test.scheduler_test import start_test
from fastapi.staticfiles import StaticFiles

load_dotenv()

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
    uvicorn.run(app, host=f"{os.getenv('HOST')}", port=int(os.getenv("PORT")))