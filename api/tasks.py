from fastapi import APIRouter, HTTPException, Depends, status
from models import TaskCreate, TaskUpdate, TaskResponse, TaskDeleteResponse
from typing import List
from pydantic import ValidationError
from service import create_task, get_task, get_tasks, update_task, delete_task, delete_task, get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.post("", response_model=TaskResponse)
async def create_task_endpoint(task: TaskCreate, current_user: dict = Depends(get_current_user,use_cache=True)):
    return create_task(task, current_user)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_endpoint(task_id: str):
    result = get_task(task_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task dengan id: {task_id} tidak ditemukan")
    return result

@router.get("", response_model=List[TaskResponse])
async def get_tasks_endpoint():
    result = get_tasks()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task tidak ditemukan")
    return result

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(task_id: str, updated_task: TaskUpdate, current_user: dict = Depends(get_current_user)):
    try:
        result = update_task(task_id, updated_task, current_user)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task tidak ditemukan")
        return result
    except ValidationError as e:
        print(e.json())
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validasi error")

@router.delete("/{task_id}", response_model=TaskDeleteResponse)
async def delete_task_endpoint(task_id: str, current_user: dict = Depends(get_current_user)):
    result = delete_task(task_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task tidak ditemukan")
    return result