
from fastapi import FastAPI
import uvicorn
import models
from database import engine
import note

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(note.router, prefix="/api/notes")

@app.get("/api/check")
def root():
    return {"message": "Hello world!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)