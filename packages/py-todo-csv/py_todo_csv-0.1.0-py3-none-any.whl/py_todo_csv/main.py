import os
import platform
import typer
import pandas as pd
from tabulate import tabulate

app = typer.Typer(help="The simplest python ToDo cli app")

pasta = os.path.dirname(os.path.abspath(__file__))
caminho_csv = os.path.join(pasta, ".list.csv")

sys = platform.system()



@app.command()
def view():
    """
    Views the current ToDos, whether marked or unmarked.
    If the user didn't add any ToDos, it creates an empty ToDo list.
    If the user finishes all tasks, it clears the file.
    """
    try:
        file = pd.read_csv(caminho_csv, sep=",")
        # all_done condition to clear the file
        all_done = False
        empty = file["Finished"].isnull().all()
        if file["Finished"].all() and not empty:
            all_done = True
        # change true/false to cool emojis
        emoji_map = {True: "✅", False: "❌"}
        file["Finished"] = file["Finished"].map(emoji_map)
        if not empty:
            if sys == "Windows":
                os.system("cls")
            else:
                os.system("clear")
            print(
                f'{tabulate(file, headers=file.head(), tablefmt="simple",showindex="always")}\n'
            )
            if all_done:
                print("You've finished all of your tasks!")
                os.remove(caminho_csv)
                with open(caminho_csv, "w") as file:
                    file.write("Task,Finished")

    except FileNotFoundError:
        with open(caminho_csv, "w") as file:
            print("You didn't add any ToDos!")
            file.write("Task,Finished")


@app.command()
def add(item: str):
    """
    Adds a new todo at the bottom at the list

    Usage: add "your todo here"
    """
    with open(caminho_csv, "a+") as file:
        file.write(f"\n{item},False")


@app.command()
def mark(row: int):
    """
    Marks one of your tasks

    Example: mark 2 3
    Then the rows 2 and 3 will be checked
    """
    try:
        file = pd.read_csv(caminho_csv)
        if 0 <= row < len(file):
            if not file.at[row, "Finished"]:
                file.at[row, "Finished"] = True
                file.to_csv(caminho_csv, index=False)
            else:
                print(f"Task {row} was already finished!")
        else:
            print("Please inform a valid row")
    except FileNotFoundError:
        with open(caminho_csv, "w") as file:
            file.write("Task,Finished")


@app.command()
def rename(row: int, task: str):
    """
    Renames one of your current tasks
    Example: rename 2 "your todo"
    Then the task with index 2 will be renamed to "your todo" (without quotes)
    """
    try:
        file = pd.read_csv(caminho_csv)
        if 0 <= row < len(file):
            file.at[row, "Task"] = task
            file.to_csv(caminho_csv, index=False)
            print("The task was renamed")
        else:
            print("Please inform a valid row")
    except FileNotFoundError:
        with open(caminho_csv, "w") as file:
            file.write("Task,Finished")
