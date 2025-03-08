import tkinter as tk
from tkinter import ttk, messagebox
import os

# Window Setup
root = tk.Tk()
root.title("To Do List")
root.geometry("500x600")
root.resizable(False, False)

# Style Configuration
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=6)
style.configure("TLabel", font=("Arial", 14), padding=5)
style.configure("TEntry", font=("Arial", 12), padding=5)
style.configure("TListbox", font=("Arial", 12))

# Undo Stack
undo_stack = []

# Add Task Function
def add_task(event=None):
    task = task_entry.get()
    if task:
        task_listbox.insert(tk.END, task)
        undo_stack.append(("add", task))
        task_entry.delete(0,tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task.")

# Delete Task Function
def delete_task():
    selected_task = task_listbox.curselection()
    if selected_task:
        task = task_listbox.get(selected_task)
        undo_stack.append(("delete", selected_task[0], task))
        task_listbox.delete(selected_task)
    else:
        messagebox.showwarning("Warning", "Select a task to delete")

# Undo Last Action
def undo_last_action():
    if undo_stack:
        last_action = undo_stack.pop()
        if last_action[0] == "add":
            for i in range(task_listbox.size() - 1, -1, -1):
                if task_listbox.get(i) == last_action[1]:
                    task_listbox.delete(i)
                    break
        elif last_action[0] == "delete":
            task_listbox.insert(last_action[1], last_action[2])
    else:
        messagebox.showwarning("Warning", "There is no action to undo.")

# Clear All Tasks
def clear_all_tasks():
    task_listbox.delete(0, tk.END)

# Save Tasks
def save_tasks():
    folder_path = r"C:\Users\Abdullah Yağmur\OneDrive\Desktop\Intermediate Python\mini python projects\to_do_list_project"
    file_path = os.path.join(folder_path, "tasks.txt")
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    tasks = task_listbox.get(0, tk.END)
    with open(file_path, "w", encoding="utf-8") as f:
        for task in tasks:
            f.write(task + "\n")
    messagebox.showinfo("Success", "Tasks saved successfully.")

# Load Tasks
def load_tasks():
    folder_path = r"C:\Users\Abdullah Yağmur\OneDrive\Desktop\Intermediate Python\mini python projects\to_do_list_project"
    file_path = os.path.join(folder_path, "tasks.txt")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tasks = f.readlines()
            for task in tasks:
                task_listbox.insert(tk.END, task.strip())
    except FileNotFoundError:
        messagebox.showwarning("Warning", "No tasks found.")

# Title Label
title_label = ttk.Label(root, text="To Do List", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

# Task Entry Field
task_entry = ttk.Entry(root, width=50)
task_entry.pack(pady=10)

# Task Listbox
task_listbox = tk.Listbox(root, width=50, height=15, font=("Arial", 12), selectmode=tk.SINGLE)
task_listbox.pack(pady=10)

# Button Frame
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

# Buttons
add_button = ttk.Button(button_frame, text="Add", command=add_task, width=15)
add_button.grid(row=0, column=0, padx=5, pady=5)

delete_button = ttk.Button(button_frame, text="Delete", command=delete_task, width=15)
delete_button.grid(row=0, column=1, padx=5, pady=5)

undo_button = ttk.Button(button_frame, text="Undo", command=undo_last_action, width=15)
undo_button.grid(row=1, column=0, padx=5, pady=5)

clear_button = ttk.Button(button_frame, text="Clear All", command=clear_all_tasks, width=15)
clear_button.grid(row=1, column=1, padx=5, pady=5)

save_button = ttk.Button(root, text="Save", command=save_tasks, width=20)
save_button.pack(pady=5)

load_button = ttk.Button(root, text="Load", command=load_tasks, width=20)
load_button.pack(pady=5)

# Enter Key Binding
root.bind("<Return>", lambda event: add_task())

# CTRL-Z Key Binding
root.bind("<Control-z>", lambda event: undo_last_action())

# Load Existing Tasks
load_tasks()

# Main Loop
root.mainloop()
