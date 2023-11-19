from models import TaskCreate, TaskUpdate, TaskResponse, TaskDeleteResponse
from database.connection import database
from datetime import datetime
import pytz
import uuid
from typing import List, Optional
from pymongo.results import DeleteResult

collection = database["tasks"]

def create_task(task: TaskCreate) -> TaskResponse:
    task_dict = task.dict()
    task_dict["id"] = str(uuid.uuid4())
    created_at = datetime.now(pytz.timezone("Asia/Jakarta"))
    task_dict["created_at"] = created_at
    task_dict["updated_at"] = created_at
    task_dict["deadline"] = datetime.combine(task_dict["deadline"], datetime.min.time())
    collection.insert_one(task_dict)
    new_task = TaskResponse(**task_dict)
    return new_task

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

def update_task(task_id: str, updated_task: TaskUpdate) -> TaskResponse:
    updated_dict = updated_task.dict()
    updated_dict["deadline"] = datetime.combine(updated_task.deadline, datetime.min.time())

    updated_dict["updated_at"] = datetime.now(pytz.timezone("Asia/Jakarta"))

    result = collection.update_one({"id": task_id}, {"$set": updated_dict})
    if result.modified_count == 0:
        return None
    task_data = collection.find_one({"id": task_id})
    return TaskResponse(**task_data) if task_data else None

def delete_task(task_id: str) -> TaskDeleteResponse:
    result = collection.delete_one({"id": task_id})
    if result.deleted_count == 0:
        return None
    return {"message": "Task berhasil dihapus"}

def delete_tasks() -> Optional[TaskDeleteResponse]:
    result: DeleteResult = collection.delete_many({})
    if result.deleted_count == 0:
        print("result deleted:::", result.deleted_count)
        return None
    return TaskDeleteResponse(message=f"{result.deleted_count} Task berhasil dihapus")
