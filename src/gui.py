import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Menu
from tkcalendar import DateEntry
from datetime import datetime
from db import tables, database
from sqlalchemy.orm import Session

engine = database.engine
tables.Base.metadata.create_all(bind=engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unimicro Task Manager")
        self.db = next(get_db())
        self.sort_column = None
        self.sort_reverse = False

        header = ttk.Frame(root)
        header.pack(fill="x", padx=10, pady=10)
        ttk.Label(header, text="🗂️ Task List", font=("Arial", 16, "bold")).pack(side="left")

        ttk.Button(header, text="+ Add Task", command=self.open_add_modal).pack(side="right", padx=5)
        ttk.Button(header, text="🗑️ Delete Task", command=self.delete_task).pack(side="right", padx=5)
        ttk.Button(header, text="✏️ Edit Task", command=self.open_edit_modal).pack(side="right", padx=5)

        columns = ("title", "tags", "due_date", "completed")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col.title(), command=lambda c=col: self.sort_by_column(c))
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree.bind("<Double-1>", self.toggle_complete)
        self.tree.bind("<Button-3>", self.show_context_menu)

        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="View Details", command=self.view_selected_task)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Edit Task", command=self.open_edit_modal)
        self.context_menu.add_command(label="Delete Task", command=self.delete_task)

        self.refresh_tasks()

    def sort_by_column(self, col):
        if self.sort_column == col:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = col
            self.sort_reverse = False

        tasks = self.db.query(tables.Task).all()

        def get_value(task):
            value = getattr(task, col)
            if col == "due_date":
                return value or datetime.max
            if col == "completed":
                return 1 if value else 0
            return value or ""

        sorted_tasks = sorted(tasks, key=get_value, reverse=self.sort_reverse)
        self.tree.delete(*self.tree.get_children())

        for task in sorted_tasks:
            self.tree.insert(
                "", "end", iid=task.id,
                values=(
                    task.title,
                    task.tags or "",
                    task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else "",
                    "✅" if task.completed else "❌"
                )
            )


    def refresh_tasks(self):
        self.tree.delete(*self.tree.get_children())
        tasks = self.db.query(tables.Task).all()
        for task in tasks:
            self.tree.insert(
                "", "end", iid=task.id,
                values=(
                    task.title,
                    task.tags or "",
                    task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else "",
                    "✅" if task.completed else "❌"
                )
            )

    def open_add_modal(self):
        self.open_task_modal(title="Add Task", mode="add")

    def open_edit_modal(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Task", "Please select a task to edit.")
            return

        task_id = int(selected[0])
        task = self.db.query(tables.Task).get(task_id)
        self.open_task_modal(title="Edit Task", mode="edit", task=task)

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Task", "Please select a task to delete.")
            return

        task_id = int(selected[0])
        task = self.db.query(tables.Task).get(task_id)

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{task.title}'?")
        if confirm:
            self.db.delete(task)
            self.db.commit()
            self.refresh_tasks()
            messagebox.showinfo("Deleted", "Task deleted successfully.")


    def open_task_modal(self, title, mode="add", task=None):
        modal = Toplevel(self.root)
        modal.title(title)
        modal.geometry("320x280")
        modal.resizable(False, False)
        modal.grab_set()

        ttk.Label(modal, text="Title:").pack(anchor="w", padx=10, pady=(10, 0))
        title_entry = ttk.Entry(modal, width=35)
        title_entry.pack(padx=10, pady=5)
        if task:
            title_entry.insert(0, task.title)

        ttk.Label(modal, text="Tags (comma separated):").pack(anchor="w", padx=10)
        tags_entry = ttk.Entry(modal, width=35)
        tags_entry.pack(padx=10, pady=5)
        if task and task.tags:
            tags_entry.insert(0, task.tags)

        ttk.Label(modal, text="Due Date:").pack(anchor="w", padx=10)
        due_date_entry = DateEntry(modal, date_pattern="yyyy-mm-dd")
        due_date_entry.pack(padx=10, pady=5)
        if task and task.due_date:
            due_date_entry.set_date(task.due_date.date())

        ttk.Label(modal, text="Time (HH:MM):").pack(anchor="w", padx=10)
        time_entry = ttk.Entry(modal, width=10)
        time_entry.insert(0, "12:00")
        if task and task.due_date:
            time_entry.delete(0, tk.END)
            time_entry.insert(0, task.due_date.strftime("%H:%M"))
        time_entry.pack(padx=10, pady=5)

        def save_task():
            title = title_entry.get().strip()
            if not title:
                messagebox.showerror("Error", "Title cannot be empty.")
                return

            tags = tags_entry.get().strip()
            tags = ",".join([t.strip() for t in tags.split(",")]) if tags else None

            try:
                due_date = due_date_entry.get_date()
                time_str = time_entry.get().strip()
                hour, minute = map(int, time_str.split(":"))
                due_datetime = datetime(due_date.year, due_date.month, due_date.day, hour, minute)
            except Exception:
                messagebox.showerror("Error", "Invalid time format. Use HH:MM.")
                return

            now = datetime.now()
            if mode == "add":
                new_task = tables.Task(
                    title=title,
                    tags=tags,
                    completed=False,
                    due_date=due_datetime,
                    created_at=now,
                    updated_at=now,
                )
                self.db.add(new_task)
            else:
                task.title = title
                task.tags = tags
                task.due_date = due_datetime
                task.updated_at = now

            self.db.commit()
            self.refresh_tasks()
            modal.destroy()

        button_frame = ttk.Frame(modal)
        button_frame.pack(pady=15)
        ttk.Button(button_frame, text="💾 Save", command=save_task).pack(side="left", padx=5)
        ttk.Button(button_frame, text="❌ Cancel", command=modal.destroy).pack(side="left", padx=5)


    def toggle_complete(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        task_id = int(selected[0])
        task = self.db.query(tables.Task).get(task_id)
        task.completed = not task.completed
        task.updated_at = datetime.now()
        self.db.commit()
        self.refresh_tasks()


    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def view_selected_task(self):
        selected = self.tree.selection()
        if not selected:
            return
        task_id = int(selected[0])
        task = self.db.query(tables.Task).get(task_id)
        if task:
            self.show_task_details(task)

    def show_task_details(self, task):
        modal = Toplevel(self.root)
        modal.title("Task Details")
        modal.geometry("300x250")
        modal.resizable(False, False)
        modal.grab_set()

        ttk.Label(modal, text=f"Title: {task.title}", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=5)
        ttk.Label(modal, text=f"Tags: {task.tags or '-'}").pack(anchor="w", padx=10, pady=5)
        ttk.Label(modal, text=f"Completed: {'Yes' if task.completed else 'No'}").pack(anchor="w", padx=10, pady=5)
        ttk.Label(modal, text=f"Due Date: {task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else '-'}").pack(anchor="w", padx=10, pady=5)
        ttk.Label(modal, text=f"Created At: {task.created_at.strftime('%Y-%m-%d %H:%M')}").pack(anchor="w", padx=10, pady=5)
        ttk.Label(modal, text=f"Updated At: {task.updated_at.strftime('%Y-%m-%d %H:%M')}").pack(anchor="w", padx=10, pady=5)

        ttk.Button(modal, text="Close", command=modal.destroy).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
