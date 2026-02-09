# src/cli/main.py

import argparse
from src.services.task_manager import TaskManager


def main_interactive():
    task_manager = TaskManager()
    print("Welcome to the Interactive CLI Todo App!")
    print("Type 'help' for commands, 'exit' to quit.")

    while True:
        try:
            user_input = input("todo > ").strip()
            if not user_input:
                continue

            parts = user_input.split(maxsplit=2) # Split into command, id/desc, new_desc
            command = parts[0].lower()
            
            if command == "exit":
                print("Exiting Todo App. Goodbye!")
                break
            elif command == "help":
                print("\nAvailable Commands:")
                print("  add <description>                 - Add a new task.")
                print("  list                              - List all tasks.")
                print("  complete <id>                     - Mark a task as complete.")
                print("  incomplete <id>                   - Mark a task as incomplete (active).")
                print("  update <id> <new_description>     - Update the description of a task.")
                print("  remove <id>                       - Remove a task.")
                print("  exit                              - Exit the application.")
                print("\n")
            elif command == "add":
                if len(parts) > 1:
                    description = parts[1]
                    try:
                        task = task_manager.add_task(description)
                        print(f"Added: '{task.description}' ID {task.identifier}")
                    except ValueError as e:
                        print(f"Error: {e}")
                else:
                    print("Error: 'add' command requires a description.")
            elif command == "list":
                tasks = task_manager.get_all_tasks()
                if not tasks:
                    print("No tasks in todo list.")
                else:
                    print("\nYour Todo List:")
                    for task in tasks:
                        task_display = (f"  ID: {task.identifier}, "
                                        f"Status: {task.status.capitalize()}, "
                                        f"Desc: {task.description}")
                        print(task_display)
                    print("\n")
            elif command == "complete":
                if len(parts) > 1 and parts[1].isdigit():
                    task_id = int(parts[1])
                    if task_manager.mark_task_complete(task_id):
                        print(f"Task ID {task_id} marked complete.")
                    else:
                        print(f"Error: Task ID {task_id} not found.")
                else:
                    print("Error: 'complete' command requires a valid task ID.")
            elif command == "incomplete":
                if len(parts) > 1 and parts[1].isdigit():
                    task_id = int(parts[1])
                    if task_manager.mark_task_incomplete(task_id):
                        print(f"Task ID {task_id} marked incomplete (active).")
                    else:
                        print(f"Error: Task ID {task_id} not found.")
                else:
                    print("Error: 'incomplete' command requires a valid task ID.")
            elif command == "update":
                if len(parts) > 2 and parts[1].isdigit():
                    task_id = int(parts[1])
                    new_description = parts[2]
                    try:
                        if task_manager.update_task(task_id, new_description):
                            print(f"Task ID {task_id} updated.")
                        else:
                            print(f"Error: Task ID {task_id} not found.")
                    except ValueError as e:
                        print(f"Error: {e}")
                else:
                    print("Error: 'update' command requires a task ID and new description.")
            elif command == "remove":
                if len(parts) > 1 and parts[1].isdigit():
                    task_id = int(parts[1])
                    if task_manager.remove_task(task_id):
                        print(f"Task ID {task_id} removed.")
                    else:
                        print(f"Error: Task ID {task_id} not found.")
                else:
                    print("Error: 'remove' command requires a valid task ID.")
            else:
                print(f"Unknown command: '{command}'. Type 'help' for available commands.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main_interactive()