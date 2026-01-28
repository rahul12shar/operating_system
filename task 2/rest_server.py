from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

tasks = []
task_id_counter = 1

def find_task(task_id):
    return next((task for task in tasks if task['id'] == task_id), None)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({
        'success': True,
        'count': len(tasks),
        'tasks': tasks
    }), 200

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = find_task(task_id)
    if task:
        return jsonify({'success': True, 'task': task}), 200
    else:
        return jsonify({'success': False, 'message': 'Task not found'}), 404

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'success': False, 'message': 'Title is required'}), 400
    
    new_task = {
        'id': task_id_counter,
        'title': data['title'],
        'description': data.get('description', ''),
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    
    tasks.append(new_task)
    task_id_counter += 1
    
    return jsonify({'success': True, 'message': 'Task created successfully', 'task': new_task}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({'success': False, 'message': 'Task not found'}), 404
    
    data = request.get_json()
    if 'title' in data:
        task['title'] = data['title']
    if 'description' in data:
        task['description'] = data['description']
    if 'completed' in data:
        task['completed'] = data['completed']
    
    task['updated_at'] = datetime.now().isoformat()
    return jsonify({'success': True, 'message': 'Task updated successfully', 'task': task}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({'success': False, 'message': 'Task not found'}), 404
    
    tasks.remove(task)
    return jsonify({'success': True, 'message': 'Task deleted successfully'}), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Task Manager REST API',
        'endpoints': {
            'GET /tasks': 'Get all tasks',
            'GET /tasks/<id>': 'Get specific task',
            'POST /tasks': 'Create new task',
            'PUT /tasks/<id>': 'Update task',
            'DELETE /tasks/<id>': 'Delete task'
        }
    }), 200

if __name__ == '__main__':
    print("[STARTING] REST API Server starting...")
    print("[INFO] Server running on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)