# src/cli/main.py

import argparse
from colorama import Fore, Style, init
from src.services.task_manager import TaskManager


def main_interactive():
    init() # Initialize Colorama
    task_manager = TaskManager()
    print(f"{Fore.CYAN}Welcome to the Interactive CLI Todo App!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Type 'help' for commands, 'exit' to quit.{Style.RESET_ALL}")

    while True:
        try:
            user_input = input(f"{Fore.CYAN}todo > {Style.RESET_ALL}").strip()
            if not user_input:
                continue

            parts = user_input.split(maxsplit=2) # Split into command, id/desc, new_desc
            command = parts[0].lower()
            
            if command == "exit":
                print(f"{Fore.CYAN}Exiting Todo App. Goodbye!{Style.RESET_ALL}")
                break
            elif command == "help":
                print(f"\n{Fore.CYAN}Available Commands:{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}  add <description>{Style.RESET_ALL}                 - {Fore.WHITE}Add a new task.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}  list{Style.RESET_ALL}                              - {Fore.WHITE}List all tasks.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}  complete <id>{Style.RESET_ALL}                     - {Fore.WHITE}Mark a task as complete.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}  incomplete <id>{Style.RESET_ALL}                   - {Fore.WHITE}Mark a task as incomplete (active).{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}  update <id> <new_description>{Style.RESET_ALL}     - {Fore.WHITE}Update the description of a task.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}  remove <id>{Style.RESET_ALL}                       - {Fore.WHITE}Remove a task.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}  exit{Style.RESET_ALL}                              - {Fore.WHITE}Exit the application.{Style.RESET_ALL}")
                print("\n")
            elif command == "add":
                if len(parts) > 1:
                    description = parts[1]
                    try:
                        task = task_manager.add_task(description)
                        print(f"{Fore.GREEN}Added: '{task.description}' ID {task.identifier}{Style.RESET_ALL}")
                    except ValueError as e:
                        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Error: 'add' command requires a description.{Style.RESET_ALL}")
            elif command == "list":
                tasks = task_manager.get_all_tasks()
                if not tasks:
                    print(f"{Fore.YELLOW}No tasks in todo list.{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.CYAN}Your Todo List:{Style.RESET_ALL}")
                    for task in tasks:
                        task_display = (f"  {Fore.YELLOW}ID: {task.identifier}{Style.RESET_ALL}, "
                                        f"Status: {Fore.BLUE if task.status == 'complete' else Fore.WHITE}{task.status.capitalize()}{Style.RESET_ALL}, "
                                        f"Desc: {Fore.WHITE}{task.description}{Style.RESET_ALL}")
                        print(task_display)
                    print("\n")
            elif command == "complete":
                if len(parts) > 1 and parts[1].isdigit():
                    task_id = int(parts[1])
                    if task_manager.mark_task_complete(task_id):
                        print(f"{Fore.GREEN}Task ID {task_id} marked complete.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Error: Task ID {task_id} not found.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Error: 'complete' command requires a valid task ID.{Style.RESET_ALL}")
            elif command == "incomplete":
                if len(parts) > 1 and parts[1].isdigit():
                    task_id = int(parts[1])
                    if task_manager.mark_task_incomplete(task_id):
                        print(f"{Fore.GREEN}Task ID {task_id} marked incomplete (active).{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Error: Task ID {task_id} not found.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Error: 'incomplete' command requires a valid task ID.{Style.RESET_ALL}")
            elif command == "update":
                if len(parts) > 2 and parts[1].isdigit():
                    task_id = int(parts[1])
                    new_description = parts[2]
                    try:
                        if task_manager.update_task(task_id, new_description):
                            print(f"{Fore.GREEN}Task ID {task_id} updated.{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}Error: Task ID {task_id} not found.{Style.RESET_ALL}")
                    except ValueError as e:
                        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Error: 'update' command requires a task ID and new description.{Style.RESET_ALL}")
            elif command == "remove":
                if len(parts) > 1 and parts[1].isdigit():
                    task_id = int(parts[1])
                    if task_manager.remove_task(task_id):
                        print(f"{Fore.GREEN}Task ID {task_id} removed.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Error: Task ID {task_id} not found.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Error: 'remove' command requires a valid task ID.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Unknown command: '{command}'. Type 'help' for available commands.{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main_interactive()