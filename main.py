from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "status": "online",
        "version": "1.0.0",
        "message": "mensaje de prueba para test: prueba de protección PR dev3"
    }