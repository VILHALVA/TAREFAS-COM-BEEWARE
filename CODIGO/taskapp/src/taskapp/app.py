import os
import sqlite3
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'tasks.db')

def initialize_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_database()

class TaskApp(toga.App):
    def startup(self):
        self.initialize_database()
        
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box

        self.task_input = toga.TextInput(style=Pack(flex=1))
        add_button = toga.Button('ADICIONAR', on_press=self.add_task, style=Pack(padding=5))
        update_button = toga.Button('ATUALIZAR', on_press=self.update_task, style=Pack(padding=5))
        delete_button = toga.Button('EXCLUIR', on_press=self.delete_task, style=Pack(padding=5))

        button_box = toga.Box(style=Pack(direction=ROW, padding=5))
        button_box.add(add_button)
        button_box.add(update_button)
        button_box.add(delete_button)

        main_box.add(self.task_input)
        main_box.add(button_box)

        self.task_table = toga.Table(['ID', 'Tarefa'], data=self.load_tasks(), on_select=self.on_task_select, style=Pack(flex=1))

        main_box.add(self.task_table)

        self.main_window.show()

    def initialize_database(self):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def load_tasks(self):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()

        conn.close()
        return [(str(task[0]), task[1]) for task in tasks]

    def add_task(self, widget):
        task_text = self.task_input.value.strip()
        if task_text:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task_text,))
            conn.commit()
            conn.close()
            self.task_table.data = self.load_tasks()
            self.task_input.value = ''

    def update_task(self, widget):
        selected_row = self.task_table.selection
        if selected_row is not None:
            task_id = selected_row.id  
            new_task_text = self.task_input.value.strip()
            if new_task_text:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                cursor.execute('UPDATE tasks SET task = ? WHERE id = ?', (new_task_text, task_id))
                conn.commit()
                conn.close()
                self.task_table.data = self.load_tasks()
                self.task_input.value = ''

    def delete_task(self, widget):
        selected_row = self.task_table.selection
        if selected_row is not None:
            task_id = selected_row.id  

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            conn.close()
            self.task_table.data = self.load_tasks()

    def on_task_select(self, widget, selection):
        if selection:
            selected_row = selection[0]
            task_id = int(selected_row[0])  
            self.task_input.value = selected_row[1]  
            print(f"Selected Task ID: {task_id}, Task Name: {selected_row[1]}")
        else:
            self.task_input.value = ""  

def main():
    return TaskApp('taskapp', 'com.example.taskapp')

if __name__ == '__main__':
    main().main_loop()
