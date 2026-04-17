from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "status": "online",
        "version": "1.0.0",
<<<<<<< HEAD
        "message": "mensaje de prueba para test: prueba de protección PR dev"
=======
        "message": "mensaje de prueba para test: prueba de protección PR dev3"
>>>>>>> eef29d6e17c4b0fbe318b3137ca2ecc69532ea11
    }