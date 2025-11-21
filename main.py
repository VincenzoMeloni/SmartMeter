from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.backend.middleware.logginMidd import Log
from app.backend.routes import sensor_routes
from app.backend.database.db import creaDB
from scheduler import start

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        creaDB()
        print("DB OK")
    except Exception as e:
        print(f"Errore DB: {str(e)}")
        raise SystemExit("Server Arrestato.")

    start()
    print("Scheduler avviato.")

    yield
    print("Server in spegnimento...")

app = FastAPI(title="SmartMeter",lifespan=lifespan)

app.add_middleware(Log)
app.include_router(sensor_routes.router)

@app.get("/")
def root():
    return {'message': 'Prova progetto IOT'}

# uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)