from tkinter import *
import json
import os

tasks = []
editing_index = None

BG = "#F3F5F2"
CARD = "#FFFFFF"
DARK = "#20352F"
GREEN = "#26866A"
GREEN_HOVER = "#329B7D"
RED = "#D95757"
RED_HOVER = "#E76B6B"
TEXT = "#263B34"
MUTED = "#82918A"


def save_tasks():
    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


def load_tasks():
    global tasks

    if os.path.exists("tasks.json"):
        try:
            with open("tasks.json", "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, list):
                tasks = data
            else:
                tasks = []

        except (json.JSONDecodeError, OSError):
            tasks = []

    show_tasks()


def show_tasks():
    task_list.delete(0, END)

    for task in tasks:
        if task["done"]:
            task_list.insert(END, "   ✓    " + task["name"])
        else:
            task_list.insert(END, "   ○    " + task["name"])

    total = len(tasks)
    completed = sum(1 for task in tasks if task["done"])
    remaining = total - completed

    counter.config(
        text=f"{remaining} TASKS LEFT     •     {completed} COMPLETED"
    )

    progress = int((completed / total) * 100) if total > 0 else 0

    progress_label.config(text=f"{progress}% COMPLETED")
    progress_bar.config(width=progress * 2)


def reset_input():
    global editing_index

    editing_index = None
    task_entry.delete(0, END)
    add_button.config(text="+ ADD", command=add_task)
    cancel_button.pack_forget()


def add_task():
    name = task_entry.get().strip()

    if name:
        tasks.append({
            "name": name,
            "done": False
        })

        save_tasks()
        show_tasks()
        reset_input()


def edit_task():
    global editing_index

    selected = task_list.curselection()

    if selected:
        editing_index = selected[0]

        task_entry.delete(0, END)
        task_entry.insert(0, tasks[editing_index]["name"])

        add_button.config(text="SAVE", command=save_edit)
        cancel_button.pack(side="right", padx=5, ipady=7)


def save_edit():
    global editing_index

    if editing_index is not None:
        new_name = task_entry.get().strip()

        if new_name:
            tasks[editing_index]["name"] = new_name

            save_tasks()
            show_tasks()
            reset_input()


def delete_task():
    selected = task_list.curselection()

    if selected:
        tasks.pop(selected[0])

        save_tasks()
        show_tasks()
        reset_input()


def toggle_task():
    selected = task_list.curselection()

    if selected:
        index = selected[0]
        tasks[index]["done"] = not tasks[index]["done"]

        save_tasks()
        show_tasks()


def clear_completed():
    global tasks

    tasks = [task for task in tasks if not task["done"]]

    save_tasks()
    show_tasks()
    reset_input()


def make_button(parent, text, command, bg, hover, fg="white"):

    button = Button(
        parent,
        text=text,
        font=("Arial", 10, "bold"),
        bg=bg,
        fg=fg,
        activebackground=hover,
        activeforeground=fg,
        relief="flat",
        bd=0,
        cursor="hand2",
        command=command
    )

    button.bind(
        "<Enter>",
        lambda event: button.config(bg=hover)
    )

    button.bind(
        "<Leave>",
        lambda event: button.config(bg=bg)
    )

    return button


gui = Tk()
gui.title("My Daily Tasks")
gui.geometry("460x680")
gui.minsize(380, 580)
gui.configure(bg=BG)


header = Frame(gui, bg=DARK)
header.pack(fill="x")

Label(
    header,
    text="DAILY PLANNER",
    font=("Arial", 22, "bold"),
    bg=DARK,
    fg="white"
).pack(anchor="w", padx=25, pady=(25, 5))

Label(
    header,
    text="Organize your day. Get things done.",
    font=("Arial", 10),
    bg=DARK,
    fg="#B8CEC4"
).pack(anchor="w", padx=27, pady=(0, 25))


main_frame = Frame(gui, bg=BG)
main_frame.pack(fill="both", expand=True, padx=22, pady=18)


Label(
    main_frame,
    text="NEW TASK",
    font=("Arial", 10, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w", pady=(0, 8))


input_frame = Frame(main_frame, bg=CARD)
input_frame.pack(fill="x", pady=(0, 20))

task_entry = Entry(
    input_frame,
    font=("Arial", 12),
    bg=CARD,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    bd=0
)
task_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=14,
    pady=14
)


add_button = make_button(
    input_frame,
    "+ ADD",
    add_task,
    GREEN,
    GREEN_HOVER
)
add_button.pack(side="right", padx=8, pady=7, ipadx=10, ipady=7)


cancel_button = make_button(
    input_frame,
    "CANCEL",
    reset_input,
    "#E5EBE7",
    "#D5E1DA",
    DARK
)


progress_frame = Frame(main_frame, bg=CARD)
progress_frame.pack(fill="x", pady=(0, 18))

Label(
    progress_frame,
    text="YOUR PROGRESS",
    font=("Arial", 10, "bold"),
    bg=CARD,
    fg=TEXT
).pack(side="left", padx=14, pady=14)

progress_label = Label(
    progress_frame,
    text="0% COMPLETED",
    font=("Arial", 9, "bold"),
    bg=CARD,
    fg=GREEN
)
progress_label.pack(side="right", padx=14)

progress_track = Frame(
    progress_frame,
    bg="#E5EBE7",
    height=7
)
progress_track.pack(fill="x", padx=14, pady=(0, 14))
progress_track.pack_propagate(False)

progress_bar = Frame(
    progress_track,
    bg=GREEN,
    width=0,
    height=7
)
progress_bar.pack(side="left", fill="y")


Label(
    main_frame,
    text="MY TASKS",
    font=("Arial", 10, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w", pady=(0, 8))

list_frame = Frame(main_frame, bg=CARD)
list_frame.pack(fill="both", expand=True)

task_list = Listbox(
    list_frame,
    font=("Arial", 12),
    bg=CARD,
    fg=TEXT,
    selectbackground="#DCEDE5",
    selectforeground=DARK,
    relief="flat",
    bd=0,
    activestyle="none",
    highlightthickness=0
)
task_list.pack(
    fill="both",
    expand=True,
    padx=12,
    pady=12
)


action_frame = Frame(main_frame, bg=BG)
action_frame.pack(fill="x", pady=15)

done_button = make_button(
    action_frame,
    "DONE / UNDO",
    toggle_task,
    GREEN,
    GREEN_HOVER
)
done_button.pack(
    side="left",
    fill="x",
    expand=True,
    padx=3,
    ipady=10
)

edit_button = make_button(
    action_frame,
    "EDIT",
    edit_task,
    "#496C91",
    "#5C83AB"
)
edit_button.pack(
    side="left",
    fill="x",
    expand=True,
    padx=3,
    ipady=10
)

delete_button = make_button(
    action_frame,
    "DELETE",
    delete_task,
    RED,
    RED_HOVER
)
delete_button.pack(
    side="right",
    fill="x",
    expand=True,
    padx=3,
    ipady=10
)


clear_button = make_button(
    main_frame,
    "CLEAR COMPLETED TASKS",
    clear_completed,
    "#E5EBE7",
    "#D5E1DA",
    DARK
)
clear_button.pack(fill="x", ipady=9)


counter = Label(
    gui,
    text="0 TASKS LEFT     •     0 COMPLETED",
    font=("Arial", 9, "bold"),
    bg=BG,
    fg=MUTED
)
counter.pack(pady=12)


task_entry.bind(
    "<Return>",
    lambda event: save_edit() if editing_index is not None else add_task()
)

load_tasks()

gui.mainloop()