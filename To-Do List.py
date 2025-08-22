import os
import json
from datetime import datetime
import re

class ToDoList:
    def __init__(self, filename="todo_list.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Load tasks from the JSON file with error handling."""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            print("Error loading tasks. Starting with an empty list.")
            return []

    def save_tasks(self):
        """Save tasks to the JSON file with error handling."""
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.tasks, file, indent=4)
        except IOError:
            print("Error saving tasks.")

    def add_task(self, description, priority=1, due_date=None):
        """Add a new task with priority and due date."""
        if not description.strip():
            print("Task description cannot be empty.")
            return
        if not isinstance(priority, int) or not 1 <= priority <= 3:
            print("Priority must be an integer between 1 and 3.")
            return
        if due_date and not self.validate_date(due_date):
            print("Invalid due date format. Use YYYY-MM-DD.")
            return

        task = {
            'id': self._get_next_id(),
            'description': description.strip(),
            'priority': priority,
            'due_date': due_date,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'completed': False
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"Task added: {description} (Priority: {priority}, Due: {due_date or 'None'})")

    def _get_next_id(self):
        """Generate the next task ID."""
        return max([task['id'] for task in self.tasks], default=0) + 1

    def validate_date(self, date_str):
        """Validate date format (YYYY-MM-DD)."""
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(pattern, date_str):
            return False
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def view_tasks(self, show_completed=False):
        """Display tasks, optionally filtering completed ones."""
        if not self.tasks:
            print("No tasks in the list.")
            return
        sorted_tasks = sorted(self.tasks, key=lambda x: (x['completed'], -x['priority'], x['due_date'] or '9999-12-31'))
        for task in sorted_tasks:
            if not show_completed and task['completed']:
                continue
            status = "✓" if task['completed'] else " "
            priority = f"[Priority: {task['priority']}]"
            due = f"(Due: {task['due_date'] or 'None'})"
            print(f"[{status}] {task['id']}: {task['description']} {priority} {due} (Created: {task['created_at']})")

    def update_task(self, task_id, description=None, priority=None, due_date=None, completed=None):
        """Update a task's details."""
        for task in self.tasks:
            if task['id'] == task_id:
                if description and description.strip():
                    task['description'] = description.strip()
                if priority and 1 <= priority <= 3:
                    task['priority'] = priority
                if due_date and self.validate_date(due_date):
                    task['due_date'] = due_date
                elif due_date == "":
                    task['due_date'] = None
                if completed is not None:
                    task['completed'] = completed
                self.save_tasks()
                print(f"Task {task_id} updated.")
                return
        print(f"Task {task_id} not found.")

    def delete_task(self, task_id):
        """Delete a task from the list."""
        initial_len = len(self.tasks)
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        if len(self.tasks) < initial_len:
            self.save_tasks()
            print(f"Task {task_id} deleted.")
        else:
            print(f"Task {task_id} not found.")

def main():
    todo = ToDoList()
    
    while True:
        print("\nTo-Do List Manager")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. View Completed Tasks")
        print("4. Update Task")
        print("5. Delete Task")
        print("6. Mark Task as Complete")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            description = input("Enter task description: ").strip()
            priority_input = input("Enter priority (1-3, default 1): ").strip()
            try:
                priority = int(priority_input) if priority_input and priority_input.isdigit() else 1
            except ValueError:
                print("Invalid priority. Using default priority 1.")
                priority = 1
            due_date = input("Enter due date (YYYY-MM-DD, press Enter to skip): ").strip()
            due_date = due_date if due_date else None
            todo.add_task(description, priority, due_date)
        
        elif choice == "2":
            todo.view_tasks()
        
        elif choice == "3":
            todo.view_tasks(show_completed=True)
        
        elif choice == "4":
            try:
                task_id = int(input("Enter task ID to update: "))
                description = input("Enter new description (press Enter to skip): ").strip()
                priority_input = input("Enter new priority (1-3, press Enter to skip): ").strip()
                priority = int(priority_input) if priority_input and priority_input.isdigit() else None
                due_date = input("Enter new due date (YYYY-MM-DD, press Enter to skip): ").strip()
                due_date = due_date if due_date else None
                todo.update_task(task_id, description, priority, due_date)
            except ValueError:
                print("Please enter a valid task ID.")
        
        elif choice == "5":
            try:
                task_id = int(input("Enter task ID to delete: "))
                todo.delete_task(task_id)
            except ValueError:
                print("Please enter a valid task ID.")
        
        elif choice == "6":
            try:
                task_id = int(input("Enter task ID to mark as complete: "))
                todo.update_task(task_id, completed=True)
            except ValueError:
                print("Please enter a valid task ID.")
        
        elif choice == "7":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()