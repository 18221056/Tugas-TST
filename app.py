from fastapi import FastAPI
from api import api_router

app = FastAPI()

@app.get("/")
async def home():
    result = {
        'status': 200,
        'message': "Hello, world!"
    }
    return result

app.include_router(api_router, prefix="/api")