import os
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

# Create 'data' folder inside the same folder as the script
folder = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(folder):
    os.makedirs(folder)

# Path for tasks.txt
TASKS_FILE = os.path.join(folder, "tasks.txt")

# Load tasks from file
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        tasks = [line.strip() for line in f.readlines()]
    return tasks

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        for task in tasks:
            f.write(task + "\n")

# Display tasks with colors and sorting
def show_tasks(tasks):
    if not tasks:
        print("No tasks in your to-do list.\n")
        return

    # Separate pending and done tasks
    pending = [t for t in tasks if t.startswith("[ ]")]
    done = [t for t in tasks if t.startswith("[✔]")]

    print("\nYour To-Do List:")
    for i, task in enumerate(pending + done, start=1):
        if task.startswith("[✔]"):
            print(Fore.GREEN + f"{i}. {task}")
        else:
            print(Fore.YELLOW + f"{i}. {task}")
    print()

def main():
    tasks = load_tasks()
    while True:
        print("Options: add / view / delete / done / quit")
        choice = input("Enter your choice: ").lower()

        if choice == "add":
            task_name = input("Enter task name: ")
            due_date = input("Enter due date (YYYY-MM-DD) or leave blank: ")
            if due_date:
                try:
                    datetime.strptime(due_date, "%Y-%m-%d")
                except ValueError:
                    print("Invalid date format! Task added without due date.")
                    due_date = ""
            task_entry = f"[ ] {task_name}"
            if due_date:
                task_entry += f" (Due: {due_date})"
            tasks.append(task_entry)
            save_tasks(tasks)
            print(f"Task '{task_name}' added!\n")

        elif choice == "view":
            show_tasks(tasks)

        elif choice == "delete":
            show_tasks(tasks)
            if tasks:
                try:
                    task_num = int(input("Enter the task number to delete: "))
                    if 1 <= task_num <= len(tasks):
                        removed = tasks.pop(task_num - 1)
                        save_tasks(tasks)
                        print(f"Task '{removed}' deleted!\n")
                    else:
                        print("Invalid task number!\n")
                except ValueError:
                    print("Please enter a valid number!\n")

        elif choice == "done":
            show_tasks(tasks)
            if tasks:
                try:
                    task_num = int(input("Enter the task number you completed: "))
                    if 1 <= task_num <= len(tasks):
                        task = tasks[task_num - 1]
                        if task.startswith("[ ]"):
                            tasks[task_num - 1] = "[✔]" + task[3:]
                            save_tasks(tasks)
                            print(f"Task '{task[4:]}' marked as done!\n")
                        else:
                            print("Task is already done!\n")
                    else:
                        print("Invalid task number!\n")
                except ValueError:
                    print("Please enter a valid number!\n")

        elif choice == "quit":
            print("Exiting To-Do List. Goodbye!")
            break

        else:
            print("Invalid option! Please try again.\n")

if __name__ == "__main__":
    main()
