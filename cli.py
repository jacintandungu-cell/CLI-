import argparse
from rich.console import Console
from rich.table import Table
from storage.file_manager import load_data, save_data

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Project Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")


    user_parser = subparsers.add_parser("add-user")
    user_parser.add_argument("username")
    user_parser.add_argument("email")
    subparsers.add_parser("list-users")

    
    project_parser = subparsers.add_parser("add-project")
    project_parser.add_argument("username")
    project_parser.add_argument("project_name")
    project_parser.add_argument("description")

    list_projects = subparsers.add_parser("list-projects")
    list_projects.add_argument("--user", help="Filter by username")

    
    task_parser = subparsers.add_parser("add-task")
    task_parser.add_argument("project_name")
    task_parser.add_argument("title")
    task_parser.add_argument("due_date")

    complete_parser = subparsers.add_parser("complete-task")
    complete_parser.add_argument("project_name")
    complete_parser.add_argument("title")

    list_tasks = subparsers.add_parser("list-tasks")
    list_tasks.add_argument("--user", help="Filter by username")
    list_tasks.add_argument("--project", help="Filter by project name")

    args = parser.parse_args()
    data = load_data()

    if args.command == "add-user":
        data["users"].append({"username": args.username, "email": args.email, "projects": []})
        save_data(data)
        console.print(f"[green]User {args.username} added.[/green]")

    elif args.command == "list-users":
        table = Table(title="Users")
        table.add_column("Username", style="cyan")
        table.add_column("Email", style="magenta")
        for user in data["users"]:
            table.add_row(user["username"], user["email"])
        console.print(table)

    elif args.command == "add-project":
        for user in data["users"]:
            if user["username"] == args.username:
                user["projects"].append({"name": args.project_name, "description": args.description, "tasks": []})
                save_data(data)
                console.print(f"[green]Project {args.project_name} added to {args.username}.[/green]")
                break

    elif args.command == "list-projects":
        table = Table(title="Projects")
        table.add_column("User", style="cyan")
        table.add_column("Project Name", style="green")
        table.add_column("Description", style="yellow")
        for user in data["users"]:
            if args.user and user["username"] != args.user:
                continue
            for project in user["projects"]:
                table.add_row(user["username"], project["name"], project["description"])
        console.print(table)

    elif args.command == "add-task":
        for user in data["users"]:
            for project in user["projects"]:
                if project["name"] == args.project_name:
                    project["tasks"].append({"title": args.title, "due_date": args.due_date, "completed": False})
                    save_data(data)
                    console.print(f"[green]Task {args.title} added to {args.project_name}.[/green]")
                    return

    elif args.command == "complete-task":
        for user in data["users"]:
            for project in user["projects"]:
                if project["name"] == args.project_name:
                    for task in project["tasks"]:
                        if task["title"] == args.title:
                            task["completed"] = True
                            save_data(data)
                            console.print(f"[blue]Task {args.title} marked complete.[/blue]")
                            return

    elif args.command == "list-tasks":
        table = Table(title="Tasks")
        table.add_column("User", style="cyan")
        table.add_column("Project", style="green")
        table.add_column("Task Title", style="yellow")
        table.add_column("Due Date", style="magenta")
        table.add_column("Completed", style="red")
        for user in data["users"]:
            if args.user and user["username"] != args.user:
                continue
            for project in user["projects"]:
                if args.project and project["name"] != args.project:
                    continue
                for task in project["tasks"]:
                    status = "✅" if task["completed"] else "❌"
                    table.add_row(user["username"], project["name"], task["title"], task["due_date"], status)
        console.print(table)

if __name__ == "__main__":
    main()
