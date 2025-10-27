
from datetime import datetime
import requests

BASE_URL = "http://127.0.0.1:8000/tasks"


def get_all_tasks():
    r = requests.get(BASE_URL)
    tasks = r.json()
    if not tasks:
        print("\nNo tasks found.")
    else:
        print("\nTasks:")
        for t in tasks:
            status = "✅" if t["completed"] else "❌"
            print(f"{t['id']}: {t['title']} | tags : {t['tags']} | {t['due_date']} | completed : {status}")


def get_filtered_tasks(query: str = "", completed: bool | None = None):
    params = {}
    if query:
        params["query"] = query
    if completed is not None:
        params["completed"] = str(completed).lower()
    r = requests.get(BASE_URL, params=params)
    tasks = r.json()
    if not tasks:
        print("\nNo tasks found with the given filters.")
    else:
        print("\nFiltered Tasks:")
        for t in tasks:
            status = "✅" if t["completed"] else "❌"
            print(f"{t['id']}: {t['title']} | tags : {t['tags']} | {t['due_date']} | completed : {status}")


def create_task():
    title = input("Enter task title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    tags = input("Enter tag(s) use komma to seperate: ").strip()
    due_date_input = input("Enter due date (YYYY-MM-DD HH:MM): ")  # e.g. 2025-11-01 15:30

    if due_date_input:
        try:
            due_date = datetime.strptime(due_date_input, "%Y-%m-%d %H:%M").isoformat()
        except ValueError:
            print("⚠️ Invalid date format. Use YYYY-MM-DD HH:MM (e.g. 2025-11-01 15:30).")
            return
    else:
        due_date = None

    print(f"Due date set to: {due_date}")
    r = requests.post(BASE_URL, json={"title": title, "due_date": due_date or None, "tags": tags})
    if r.status_code == 201:
        print("Task created successfully!")
    else:
        print(f"Error: {r.status_code} {r.text}")

def delete_task():
    task_id = input("Enter task ID to delete: ").strip()
    r = requests.delete(f"{BASE_URL}/{task_id}")
    if r.status_code == 204:
        print("Task deleted successfully!")
    else:
        print(f"Error: {r.status_code} {r.text}")

def update_task():
    task_id = input("Enter task ID to update: ").strip()
    title = input("Enter new title (leave empty to keep unchanged): ").strip()
    tags = input("Enter new tags (leave empty to keep unchanged): ").strip()
    due_date_input = input("Enter new due date (YYYY-MM-DD HH:MM) (leave empty to keep unchanged): ").strip()
    completed_inp = input("Mark as completed? (y/n/skip): ").strip().lower()

    completed = None
    if completed_inp == "y":
        completed = True
    elif completed_inp == "n":
        completed = False

    if due_date_input:
        try:
            due_date = datetime.strptime(due_date_input, "%Y-%m-%d %H:%M").isoformat()
        except ValueError:
            print("⚠️ Invalid date format. Use YYYY-MM-DD HH:MM (e.g. 2025-11-01 15:30).")
            return
    else:
        due_date = None

    update_data = {}
    if title:
        update_data["title"] = title
    if tags:
        update_data["tags"] = tags
    if completed is not None:
        update_data["completed"] = completed
    if due_date is not None:
        update_data["due_date"] = due_date

    r = requests.put(f"{BASE_URL}/{task_id}", json=update_data)
    if r.status_code == 200:
        print("Task updated successfully!")
    else:
        print(f"Error: {r.status_code} {r.text}")

def cli():
    while True:
        print("\n=== TODO CLI ===")
        print("1. List all tasks")
        print("2. Seatch for tasks with filters (query, completed)")
        print("3. Create task")
        print("4. Update task")
        print("5. Delete task")


        inp = input("Choose an option (q to quit): ").strip().lower()
        if inp == "1":
            get_all_tasks()
        elif inp == "2":
            query = input("Enter search query (leave empty for none): ").strip()
            comp_inp = input("Filter by completion status? (y/n): ").strip().lower()
            completed = None
            if comp_inp == "y":
                status_inp = input("Show only completed tasks? (y/n): ").strip().lower()
                completed = True if status_inp == "y" else False
            get_filtered_tasks(query=query, completed=completed)
        elif inp == "3":
            create_task()
        elif inp == "4":
            update_task()
        elif inp == "5":
            delete_task()
        elif inp == "q":
            break
        else:
            print("Invalid option. Please try again.")



if __name__ == "__main__":
    cli()