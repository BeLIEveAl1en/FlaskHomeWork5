from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError, Field
from typing import List, Optional

app = Flask(__name__)


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


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        return jsonify(task)
    else:
        return jsonify({"error": "Task not found"}), 404


@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        task_input = TaskInput(**request.json)
        task = Task(id=len(tasks) + 1, **task_input.dict(), status=False)
        tasks.append(task.dict())
        return jsonify(task.dict()), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        try:
            task_input = TaskInput(**request.json)
            task.update(task_input.dict())
            return jsonify(task), 200
        except ValidationError as e:
            return jsonify({"error": e.errors()}), 400
    else:
        return jsonify({"error": "Task not found"}), 404


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
