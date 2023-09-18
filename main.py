import tkinter as tk
from functools import partial
from tkinter import messagebox
from tkinter import ttk
from sqlite3 import Connection, Cursor
from tkinter.ttk import Treeview, Entry

WIDTH = 60


def connect_db() -> tuple[Connection, Cursor]:
    conn = Connection("todo.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            task TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn, cursor


# Function to add a task to the database
def add_task(
        task_entry: Entry,
        task_list: Treeview,
        conn: Connection,
        cursor: Cursor
) -> None:
    task = task_entry.get()
    if task:
        cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
        task_list.insert("", "end", values=(task,))
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Task cannot be empty.")


def remove_task(
        task_list: Treeview,
        conn: Connection,
        cursor: Cursor,
) -> None:
    selected_item = task_list.selection()
    if selected_item:
        for item in selected_item:
            item_id = task_list.item(item, "values")[0]
            cursor.execute("DELETE FROM tasks WHERE id=?", (item_id,))
            conn.commit()
            task_list.delete(item)
    else:
        messagebox.showwarning("Warning", "Please select a task to remove.")


def run() -> None:
    conn, cursor = connect_db()
    root = tk.Tk()
    root.title("Daily Tasks")
    root.geometry("800x600")
    root.configure(
        background="#242424"
    )

    task_label = tk.Label(
        root,
        text="Daily Tasks",
        foreground="white",
        background="#242424",
        font=("Arial", 25)
    )
    task_label.pack(pady=(55, 30))
    task_entry = Entry(root, width=WIDTH, background="#343638", foreground="white")
    task_entry.pack(ipadx=10)

    task_list_frame = tk.Frame(root, width=WIDTH)
    task_list_frame.pack()

    task_list = Treeview(task_list_frame, columns=("Task",), show="tree")
    task_list.pack(side=tk.LEFT, fill=tk.Y)

    task_list_scrollbar = ttk.Scrollbar(task_list_frame, orient=tk.VERTICAL, command=task_list.yview, )
    task_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    task_list.column("Task", anchor=tk.W, width=WIDTH * 5, minwidth=WIDTH * 5)
    task_list.configure(yscrollcommand=task_list_scrollbar.set)

    add_button = tk.Button(
        root,
        text="Add",
        command=partial(add_task, task_entry, task_list, conn, cursor),
        width=WIDTH,
        background="#1f6aa5",
        foreground="white",
    )
    add_button.pack(pady=(32, 0))

    remove_button = tk.Button(
        root,
        text="Delete",
        command=partial(remove_task, task_list, conn, cursor),
        width=WIDTH,
        background="#1f6aa5",
        foreground="white",
    )
    remove_button.pack(pady=(32, 0))

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    for task in tasks:
        task_list.insert("", "end", values=(task[0],))

    root.mainloop()
    conn.close()


if __name__ == "__main__":
    run()
