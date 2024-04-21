from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: bool


class TaskInput(BaseModel):
    title: str = Field(..., description="Title of the task")
    description: str = Field(..., description="Description of the task")
    status: Optional[bool] = Field(None, description="Status of the task (True for completed, False for not completed)")


tasks = []


@app.get('/tasks', response_model=List[Task])
def get_tasks():
    return tasks


@app.get('/tasks/{task_id}', response_model=Task)
def get_task(task_id: int):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        return task
    else:
        raise HTTPException(status_code=404, detail="Task not found")


@app.post('/tasks', response_model=Task)
def create_task(task_input: TaskInput):
    task = Task(id=len(tasks) + 1, **task_input.dict(), status=False)
    tasks.append(task.dict())
    return task


@app.put('/tasks/{task_id}', response_model=Task)
def update_task(task_id: int, task_input: TaskInput):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        task.update(task_input.dict())
        return task
    else:
        raise HTTPException(status_code=404, detail="Task not found")


@app.delete('/tasks/{task_id}', status_code=204)
def delete_task(task_id: int):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
