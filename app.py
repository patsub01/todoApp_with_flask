from flask import Flask, render_template, request, redirect, url_for
import sqlite3  

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY, task TEXT NOT NULL, priority INTEGER NOT NULL, status TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks ORDER BY priority ASC')
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        task = request.form['task']
        priority = request.form['priority']
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute('INSERT INTO tasks (task, priority, status) VALUES (?, ?, ?)', (task, priority, 'Pending'))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    if request.method == 'POST':
        task = request.form['task']
        priority = request.form['priority']
        status = request.form['status']
        c.execute('UPDATE tasks SET task = ?, priority = ?, status = ? WHERE id = ?', (task, priority, status, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    c.execute('SELECT * FROM tasks WHERE id = ?', (id,))
    task = c.fetchone()
    conn.close()
    return render_template('edit_task.html', task=task)


@app.route('/delete/<int:id>')
def delete_task(id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
def complete_task(id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET status = ? WHERE id = ?', ('Completed', id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
