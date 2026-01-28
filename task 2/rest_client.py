import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

def print_response(response):
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def create_task(title, description=""):
    url = f"{BASE_URL}/tasks"
    data = {'title': title, 'description': description}
    response = requests.post(url, json=data)
    print(f"Creating task: {title}")
    print_response(response)
    return response.json()

def get_all_tasks():
    url = f"{BASE_URL}/tasks"
    response = requests.get(url)
    print("Getting all tasks:")
    print_response(response)
    return response.json()

def get_task(task_id):
    url = f"{BASE_URL}/tasks/{task_id}"
    response = requests.get(url)
    print(f"Getting task {task_id}:")
    print_response(response)
    return response.json()

def update_task(task_id, title=None, description=None, completed=None):
    url = f"{BASE_URL}/tasks/{task_id}"
    data = {}
    if title:
        data['title'] = title
    if description is not None:
        data['description'] = description
    if completed is not None:
        data['completed'] = completed
    
    response = requests.put(url, json=data)
    print(f"Updating task {task_id}:")
    print_response(response)
    return response.json()

def delete_task(task_id):
    url = f"{BASE_URL}/tasks/{task_id}"
    response = requests.delete(url)
    print(f"Deleting task {task_id}:")
    print_response(response)
    return response.json()

def main():
    print("=" * 50)
    print("REST API Client - Task Manager Demo")
    print("=" * 50)
    
    task1 = create_task("Complete IPC assignment", "Implement TCP and REST")
    task2 = create_task("Study for exam", "Review networking concepts")
    task3 = create_task("Buy groceries", "Milk, eggs, bread")
    
    get_all_tasks()
    get_task(1)
    update_task(1, completed=True)
    update_task(2, description="Review TCP, UDP, REST, and Message Queues")
    get_all_tasks()
    delete_task(3)
    get_all_tasks()

if __name__ == "__main__":
    main()