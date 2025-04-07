from flask import Flask, render_template, request, jsonify, Response
import sqlite3
import os
from datetime import datetime
import csv
from io import StringIO

app = Flask(__name__)

DB_PATH = "tasks.db"

# Custom Jinja2 filter to format datetime
def datetimeformat(value, format='%H:%M:%S'):
    if value:
        # Parse the ISO string and format it
        dt = datetime.fromisoformat(value)
        return dt.strftime(format)
    return value

# Register the filter with Jinja2
app.jinja_env.filters['datetimeformat'] = datetimeformat

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Updated table schema
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        completed BOOLEAN NOT NULL DEFAULT 0,
        priority TEXT DEFAULT 'low',
        due_date TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Sample data
    cursor.execute("SELECT COUNT(*) FROM tasks")
    if cursor.fetchone()[0] == 0:
        sample_tasks = [
            ("Finish Client Document", 0, "high", "2025-04-10", datetime.now().isoformat()),
            ("Review code", 1, "low", None, datetime.now().isoformat()),
        ]
        cursor.executemany("INSERT INTO tasks (title, completed, priority, due_date, created_at) VALUES (?, ?, ?, ?, ?)", sample_tasks)
    
    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks')
def get_tasks():
    search_query = request.args.get('search', '').lower()
    filter_type = request.args.get('', '')
    
    conn = get_db_connection()
    query = 'SELECT * FROM tasks'
    params = []
    
    if search_query:
        query += ' WHERE LOWER(title) LIKE ?'
        params.append(f'%{search_query}%')
    elif filter_type:
        if filter_type == 'completed':
            query += ' WHERE completed = 1'
        elif filter_type == 'active':
            query += ' WHERE completed = 0'
        elif filter_type == 'high':
            query += ' WHERE priority = "high"'
    
    query += ' ORDER BY completed, due_date ASC, id DESC'
    tasks = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('task_list.html', tasks=tasks)

@app.route('/tasks/add', methods=['POST'])
def add_task():
    title = request.form.get('title', '').strip()
    priority = request.form.get('priority', 'low')
    due_date = request.form.get('due_date', None)
    
    if title:
        conn = get_db_connection()
        cursor = conn.execute(
            'INSERT INTO tasks (title, completed, priority, due_date, created_at) VALUES (?, 0, ?, ?, ?)',
            (title, priority, due_date, datetime.now().isoformat())
        )
        task_id = cursor.lastrowid
        conn.commit()
        task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        conn.close()
        return render_template('task_item.html', task=task)
    return "", 400

@app.route('/tasks/<int:task_id>/toggle', methods=['PUT'])
def toggle_task(task_id):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    
    if task:
        new_status = 0 if task['completed'] else 1
        conn.execute('UPDATE tasks SET completed = ? WHERE id = ?', (new_status, task_id))
        conn.commit()
        task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        conn.close()
        return render_template('task_item.html', task=task)
    conn.close()
    return "", 404

@app.route('/tasks/<int:task_id>/priority', methods=['PUT'])
def update_priority(task_id):
    priority = request.form.get('priority', 'low')
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET priority = ? WHERE id = ?', (priority, task_id))
    conn.commit()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    return render_template('task_item.html', task=task)

@app.route('/tasks/<int:task_id>/delete', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return "" if cursor.rowcount > 0 else ("", 404)

@app.route('/tasks/bulk-delete', methods=['POST'])
def bulk_delete():
    task_ids = request.form.getlist('task_ids')
    if task_ids:
        conn = get_db_connection()
        conn.execute('DELETE FROM tasks WHERE id IN ({})'.format(','.join('?' * len(task_ids))), task_ids)
        conn.commit()
        conn.close()
    return get_tasks()

@app.route('/tasks/bulk-complete', methods=['POST'])
def bulk_complete():
    task_ids = request.form.getlist('task_ids')
    if task_ids:
        conn = get_db_connection()
        conn.execute('UPDATE tasks SET completed = 1 WHERE id IN ({})'.format(','.join('?' * len(task_ids))), task_ids)
        conn.commit()
        conn.close()
    return get_tasks()

@app.route('/tasks/export', methods=['GET'])
def export_tasks():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['ID', 'Title', 'Completed', 'Priority', 'Due Date', 'Created At'])
    for task in tasks:
        writer.writerow([task['id'], task['title'], task['completed'], task['priority'], task['due_date'], task['created_at']])
    
    return Response(si.getvalue(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=tasks.csv"})

if __name__ == '__main__':
    app.run(debug=True)