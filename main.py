from fastapi import FastAPI
from app.backend.middleware.logginMidd import Log
from app.backend.routes import sensor_routes
from app.backend.database.db import creaDB

try:
    creaDB()
    print("OK")
except Exception as e:
    print(f"Errore durante la creazione del DB: {str(e)}")
    raise SystemExit("Server Arrestato.")

app = FastAPI(title="SmartMeter")

app.add_middleware(Log)
app.include_router(sensor_routes.router)

@app.get("/")
def root():
    return {'message': 'Prova progetto IOT'}

# uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)