import sqlite3
conn = sqlite3.connect('db/data.db',check_same_thread=False)
cursor = conn.cursor()


def create_table():
	cursor.execute('CREATE TABLE IF NOT EXISTS tasks(task TEXT,task_status TEXT,task_due_date DATE)')


def add_data(task,task_status,task_due_date):
	cursor.execute('INSERT INTO tasks(task,task_status,task_due_date) VALUES (?,?,?)',(task,task_status,task_due_date))
	conn.commit()


def view_all_data():
	cursor.execute('SELECT * FROM tasks')
	data = cursor.fetchall()
	return data

def view_all_task_names():
	cursor.execute('SELECT DISTINCT task FROM tasks')
	data = cursor.fetchall()
	return data

def get_task(task):
	cursor.execute('SELECT * FROM tasks WHERE task="{}"'.format(task))
	data = cursor.fetchall()
	return data

def get_task_by_status(task_status):
	cursor.execute('SELECT * FROM tasks WHERE task_status="{}"'.format(task_status))
	data = cursor.fetchall()


def edit_task_data(new_task,new_task_status,new_task_date,task,task_status,task_due_date):
	cursor.execute("UPDATE tasks SET task =?,task_status=?,task_due_date=? WHERE task=? and task_status=? and task_due_date=? ",(new_task,new_task_status,new_task_date,task,task_status,task_due_date))
	conn.commit()
	data = cursor.fetchall()
	return data

def delete_data(task):
	cursor.execute('DELETE FROM tasks WHERE task="{}"'.format(task))
	conn.commit()