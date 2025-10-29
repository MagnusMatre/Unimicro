import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Menu
from tkcalendar import DateEntry
from datetime import datetime
import requests
import asyncio
import aiohttp

API_URL = "http://localhost:8000/tasks"

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unimicro Task Manager")

        self.all_tasks = []
        self.cached_tasks = {}
        self.sort_column = None
        self.sort_reverse = False
        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="all")

        header = ttk.Frame(root)
        header.pack(fill="x", padx=10, pady=10)
        ttk.Label(header, text="🗂️ Task List", font=("Arial", 16, "bold")).pack(side="left")

        ttk.Button(header, text="➕ Add Task", command=self.open_add_modal).pack(side="right", padx=5)
        ttk.Button(header, text="❌ Delete Task", command=self.delete_task).pack(side="right", padx=5)
        ttk.Button(header, text="✏️ Edit Task", command=self.open_edit_modal).pack(side="right", padx=5)

        control_frame = ttk.Frame(root)
        control_frame.pack(fill="x", padx=10, pady=(0, 10))

        ttk.Label(control_frame, text="Search:").pack(side="left")
        search_entry = ttk.Entry(control_frame, textvariable=self.search_var, width=25)
        search_entry.pack(side="left", padx=(5, 15))
        self.search_var.trace_add("write", lambda *args: self.filter_and_render_tasks())

        ttk.Label(control_frame, text="Filter:").pack(side="left")
        for value, text in [("all", "All"), ("completed", "Completed"), ("not_completed", "Not Completed")]:
            ttk.Radiobutton(
                control_frame, text=text, variable=self.filter_var, value=value,
                command=self.filter_and_render_tasks
            ).pack(side="left", padx=2)

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

        self.root.after(100, lambda: self.run_async(self.load_tasks_from_api))

    def run_async(self, coro_func, *args):
        """Run coroutine without blocking Tkinter"""
        asyncio.ensure_future(coro_func(*args))

    async def api_request(self, method, endpoint="", **kwargs):
        url = f"{API_URL}{endpoint}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, **kwargs) as resp:
                    resp.raise_for_status()
                    if resp.content_type == "application/json":
                        return await resp.json()
                    return None
        except aiohttp.ClientError as e:
            self.root.after(0, lambda e=e: messagebox.showerror("API Error", str(e)))
        
    def update_tree(self, tasks):
        self.tree.delete(*self.tree.get_children())
        for t in tasks:
            self.tree.insert("", "end", iid=t["id"], values=(t["title"], t.get("tags", ""), t.get("due_date", ""), "✅" if t["completed"] else "⚪"))


    async def load_tasks_from_api(self):
        tasks = await self.api_request("GET")
        if tasks is None:
            return
        self.all_tasks = tasks
        self.cached_tasks = {t["id"]: t for t in tasks}
        self.root.after(0, lambda: self.update_tree(tasks))
        self.root.after(0, self.filter_and_render_tasks)

    def filter_and_render_tasks(self):
        """Filter, sort, and render from in-memory cache"""
        tasks = list(self.all_tasks)
        query = self.search_var.get().lower()
        filter_value = self.filter_var.get()

        if query:
            tasks = [
                t for t in tasks
                if query in (t["title"] or "").lower() or query in (t["tags"] or "").lower()
            ]
        if filter_value == "completed":
            tasks = [t for t in tasks if t["completed"]]
        elif filter_value == "not_completed":
            tasks = [t for t in tasks if not t["completed"]]

        if self.sort_column:
            def get_value(task):
                value = task.get(self.sort_column)
                if self.sort_column == "due_date" and value:
                    try:
                        return datetime.fromisoformat(value)
                    except ValueError:
                        return datetime.max
                if self.sort_column == "completed":
                    return 1 if task["completed"] else 0
                return value or ""
            tasks.sort(key=get_value, reverse=self.sort_reverse)

        self.tree.delete(*self.tree.get_children())
        now = datetime.now()

        for t in tasks:
            due_date = t.get("due_date")
            completed = t.get("completed")
            row_id = self.tree.insert(
                "", "end", iid=t["id"],
                values=(
                    t["title"],
                    t.get("tags", ""),
                    datetime.fromisoformat(due_date).strftime("%Y-%m-%d %H:%M") if due_date else "",
                    "✅" if completed else "⚪"
                ),
            )
            if not completed and due_date and datetime.fromisoformat(due_date) < now:
                self.tree.item(row_id, tags=("overdue",))
        self.tree.tag_configure("overdue", background="#ffcccc")

    def sort_by_column(self, col):
        if self.sort_column == col:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = col
            self.sort_reverse = False
        self.filter_and_render_tasks()

    def open_add_modal(self):
        self.open_task_modal("Add Task")

    def open_edit_modal(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Task", "Please select a task to edit.")
            return
        task_id = selected[0]
        task = self.cached_tasks.get(int(task_id))
        if task:
            self.open_task_modal("Edit Task", task)

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Task", "Please select a task to delete.")
            return
        task_id = selected[0]
        confirm = messagebox.askyesno("Confirm Delete", "Delete this task?")
        if confirm:
            self.run_async(self._delete_task_async, task_id)

    async def _delete_task_async(self, task_id):
        await self.api_request("DELETE", f"/{task_id}")
        await self.load_tasks_from_api()

    def toggle_complete(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        task_id = selected[0]
        self.run_async(self._toggle_complete_async, task_id)

    async def _toggle_complete_async(self, task_id):
        await self.api_request("PUT", f"/{task_id}", json={"completed": not self.cached_tasks[int(task_id)]["completed"]})
        await self.load_tasks_from_api()

    async def _save_task_async(self, task_id, data, is_new):
        if is_new:
            await self.api_request("POST", "", json=data)
        else:
            await self.api_request("PUT", f"/{task_id}", json=data)
        await self.load_tasks_from_api()

    def open_task_modal(self, title, task=None):
        modal = Toplevel(self.root)
        modal.title(title)
        modal.geometry("320x280")
        modal.resizable(False, False)
        modal.grab_set()

        ttk.Label(modal, text="Title:").pack(anchor="w", padx=10, pady=(10, 0))
        title_entry = ttk.Entry(modal, width=35)
        title_entry.pack(padx=10, pady=5)
        if task:
            title_entry.insert(0, task["title"])

        ttk.Label(modal, text="Tags (comma separated):").pack(anchor="w", padx=10)
        tags_entry = ttk.Entry(modal, width=35)
        tags_entry.pack(padx=10, pady=5)
        if task and task.get("tags"):
            tags_entry.insert(0, task["tags"])

        ttk.Label(modal, text="Due Date:").pack(anchor="w", padx=10)
        due_date_entry = DateEntry(modal, date_pattern="yyyy-mm-dd")
        due_date_entry.pack(padx=10, pady=5)
        if task and task.get("due_date"):
            due_date_entry.set_date(datetime.fromisoformat(task["due_date"]).date())

        ttk.Label(modal, text="Time (HH:MM):").pack(anchor="w", padx=10)
        time_entry = ttk.Entry(modal, width=10)
        time_entry.insert(0, "12:00")
        if task and task.get("due_date"):
            time_entry.delete(0, tk.END)
            time_entry.insert(0, datetime.fromisoformat(task["due_date"]).strftime("%H:%M"))
        time_entry.pack(padx=10, pady=5)


        def save_task():
            title = title_entry.get().strip()
            if not title:
                messagebox.showerror("Error", "Title cannot be empty.")
                return
            tags = tags_entry.get().strip() or None
            try:
                due_date = due_date_entry.get_date()
                hour, minute = map(int, time_entry.get().split(":"))
                due_datetime = datetime(due_date.year, due_date.month, due_date.day, hour, minute).isoformat()
            except Exception:
                messagebox.showerror("Error", "Invalid time format. Use HH:MM.")
                return
            data = {"title": title, "tags": tags, "due_date": due_datetime}
            if task:
                self.run_async(self._save_task_async, task['id'], data, False)

            else:
                self.run_async(self._save_task_async, None, data, True)
            modal.destroy()

        ttk.Button(modal, text="💾 Save", command=save_task).pack(side="left", padx=20, pady=10)
        ttk.Button(modal, text="❌ Cancel", command=modal.destroy).pack(side="left", padx=10)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def view_selected_task(self):
        selected = self.tree.selection()
        if not selected:
            return
        task_id = selected[0]
        task = self.cached_tasks.get(int(task_id))
        self.show_task_details(task)

    def show_task_details(self, task):
        modal = Toplevel(self.root)
        modal.title("Task Details")
        modal.geometry("300x250")
        modal.resizable(False, False)
        modal.grab_set()
        ttk.Label(modal, text=f"Title: {task['title']}", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=5)
        ttk.Label(modal, text=f"Tags: {task.get('tags', '-')}").pack(anchor="w", padx=10, pady=5)
        ttk.Label(modal, text=f"Completed: {'Yes' if task['completed'] else 'No'}").pack(anchor="w", padx=10, pady=5)
        ttk.Label(modal, text=f"Due Date: {task.get('due_date', '-')}").pack(anchor="w", padx=10, pady=5)
        ttk.Label(modal, text=f"Created At: {task.get('created_at', '-')}").pack(anchor="w", padx=10, pady=5)
        ttk.Label(modal, text=f"Updated At: {task.get('updated_at', '-')}").pack(anchor="w", padx=10, pady=5)
        ttk.Button(modal, text="Close", command=modal.destroy).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)

    async def tkinter_loop():
        while True:
            root.update()
            await asyncio.sleep(0.01)

    asyncio.run(tkinter_loop())