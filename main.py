from fastapi import FastAPI

from schemas import PrescriptionCreate


app = FastAPI(title="Clinical Med Decision Support")


@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "message": "Clinical Med Decision Support is running.",
    }

