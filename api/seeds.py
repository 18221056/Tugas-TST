from fastapi import APIRouter
from service import seed_create_users, seed_create_tasks

router = APIRouter(
    prefix="/seeds",
    tags=["seeds"]
)

@router.get("/tasks")
async def seeds_tasks_enpoint():
    result = seed_create_tasks()
    return result

@router.get("/users")
async def seeds_users_enpoint():
    result = seed_create_users()
    return result

