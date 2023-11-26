from models import TaskCreate, TaskUpdate, TaskResponse, TaskDeleteResponse
from database.connection import database
from datetime import datetime
from typing import List, Optional
from pymongo.results import DeleteResult
from fastapi import status, HTTPException, Depends
from .auth import get_current_user
import pytz
import uuid

collection = database["tasks"]

def create_task(task: TaskCreate, current_user: dict = Depends(get_current_user)) -> TaskResponse:
    try:
        task_dict = task.dict()
        task_dict['user_id'] = [current_user['id']]
        task_dict["id"] = str(uuid.uuid4())
        created_at = datetime.now(pytz.timezone("Asia/Jakarta"))
        task_dict["created_at"] = created_at
        task_dict["updated_at"] = created_at
        task_dict["deadline"] = datetime.combine(task_dict["deadline"], datetime.min.time())
        collection.insert_one(task_dict)
        
        new_task = TaskResponse(**task_dict)
        return new_task
    
    except Exception as e:
        print("Error ketika membuat task:", str(e))
        raise

def get_task(task_id: str) -> TaskResponse:
    task = collection.find_one({"id": task_id})
    if task is None:
        return None
    return TaskResponse(**task)

def get_tasks() -> List[TaskResponse]:
    try:
        tasks_data = list(collection.find())
        tasks = [TaskResponse(**task_data) for task_data in tasks_data]
        return tasks
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return []

def update_task(task_id: str, updated_task: TaskUpdate, current_user: dict = Depends(get_current_user)) -> Optional[TaskResponse]:
    task = collection.find_one({"id": task_id})
    
    user_id = current_user['id']
    
    users_id_array = task.get("user_id")
    
    # Periksa apakah user_id dalam token sesuai dengan salah satu user_id terkait dengan task
    if user_id not in users_id_array:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Anda tidak memiliki izin untuk memperbarui task ini. Izin ditolak.")
    
    updated_dict = updated_task.dict()
    updated_dict["deadline"] = datetime.combine(updated_task.deadline, datetime.min.time())

    updated_dict["updated_at"] = datetime.now(pytz.timezone("Asia/Jakarta"))

    result = collection.update_one({"id": task_id}, {"$set": updated_dict})
    if result.modified_count == 0:
        return None
    task = collection.find_one({"id": task_id})

    return TaskResponse(**task) if task else None

def delete_task(task_id: str, current_user: dict = Depends(get_current_user)) -> TaskDeleteResponse:
    task = collection.find_one_and_delete({"id": task_id})
    
    # Jika task tidak ditemukan, kembalikan respons yang sesuai
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task dengan ID {task_id} tidak ditemukan.")
    
    user_id = current_user["id"]
    
    users_id_array = task.get("user_id")
    
    # Periksa apakah user_id dalam token sesuai dengan salah satu user_id terkait dengan task
    if user_id not in users_id_array:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Anda tidak memiliki izin untuk menghapus task ini. Izin ditolak.")
    
    if task.deleted_count == 0:
        return None
    return {"message": "Task berhasil dihapus"}

def delete_tasks(current_user: dict = Depends(get_current_user)) -> Optional[TaskDeleteResponse]:
    user_role = current_user['role']
        
    if user_role != "teacher":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Hanya akun denga role Teacher yang diizinkan untuk menghapus semua task. Izin ditolak.")
        
    result: DeleteResult = collection.delete_many({})
    if result.deleted_count == 0:
        print("result deleted:::", result.deleted_count)
        return None
    return TaskDeleteResponse(message=f"{result.deleted_count} Task berhasil dihapus")
