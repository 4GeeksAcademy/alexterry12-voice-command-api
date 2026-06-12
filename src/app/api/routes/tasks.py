from fastapi import APIRouter, HTTPException, status
from src.app.schemas.voice import Task, TaskCreate, TaskReplace, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])

# In-memory store: a plain list that holds our tasks.
# Resets to empty every time the server restarts — that's expected.
tasks: list[dict] = []

# Tracks the next ID to hand out, so every task gets a unique id.
next_id: int = 1


# Helper: find a task by its id, or raise a 404 if it doesn't exist.
def find_task(task_id: int) -> dict:
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found",
    )


@router.get("", response_model=list[Task])
def get_tasks() -> list[dict]:
    return tasks


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> dict:
    global next_id
    new_task = {
        "id": next_id,
        "title": payload.title,
        "done": payload.done,
    }
    tasks.append(new_task)
    next_id += 1
    return new_task


@router.put("/{task_id}", response_model=Task)
def replace_task(task_id: int, payload: TaskReplace) -> dict:
    task = find_task(task_id)
    task["title"] = payload.title
    task["done"] = payload.done
    return task


@router.patch("/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskUpdate) -> dict:
    task = find_task(task_id)
    if payload.title is not None:
        task["title"] = payload.title
    if payload.done is not None:
        task["done"] = payload.done
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int) -> dict[str, str]:
    task = find_task(task_id)
    tasks.remove(task)
    return {"message": f"Task {task_id} deleted"}