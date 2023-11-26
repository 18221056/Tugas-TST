from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    result = {
        'status': 200,
        'message': "Hello, world!"
    }
    return result

app.include_router(api_router, prefix="/api")