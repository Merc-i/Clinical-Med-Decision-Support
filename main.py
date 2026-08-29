from fastapi import FastAPI

app = FastAPI(title="Clinical Med Decision Support") 

@app.get("/")
def health_check():
    return{"status": "healthy", "message": "Clinical Med Decision Support is running."}


