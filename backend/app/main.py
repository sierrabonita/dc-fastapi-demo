from fastapi import FastAPI

from app.api.todos import router as todos_router

app = FastAPI(title="Backend API", version="1.0.0")
app.include_router(todos_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Backend"}
