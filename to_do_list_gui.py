import tkinter as tk
from tkinter import messagebox
import pickle
import os

FILE_NAME = "todo_list.pkl"

def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "rb") as file:
            data = pickle.load(file)
            # ตรวจสอบว่าข้อมูลเป็น list ของ dict หรือไม่
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                return data
            # ถ้าเป็น list ของ string (โครงสร้างเก่า) ให้แปลงเป็น dict
            elif isinstance(data, list) and all(isinstance(item, str) for item in data):
                return [{"task": item, "done": False} for item in data]
    return []

def save_tasks():
    with open(FILE_NAME, "wb") as file:
        pickle.dump(tasks, file)

def add_task():
    task = entry.get().strip()
    if task:
        tasks.append({"task": task, "done": False})
        update_list()
        entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Please enter a task!")

def toggle_task():
    try:
        index = listbox.curselection()[0]
        tasks[index]["done"] = not tasks[index]["done"]
        update_list()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task!")

def delete_task():
    try:
        index = listbox.curselection()[0]
        tasks.pop(index)
        update_list()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task!")

def update_list():
    listbox.delete(0, tk.END)
    for item in tasks:
        if item["done"]:
            listbox.insert(tk.END, "✔ " + item["task"])
            listbox.itemconfig(tk.END, {'fg': 'gray'})
        else:
            listbox.insert(tk.END, item["task"])
            listbox.itemconfig(tk.END, {'fg': 'black'})

# โหลดงานจากไฟล์ (รองรับโครงสร้างเก่า)
tasks = load_tasks()

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("📝 To-Do List")
root.geometry("400x500")

# กรอกงานใหม่
entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=10, padx=10, fill=tk.BOTH)

# ปุ่มเพิ่มงาน
add_button = tk.Button(root, text="➕ Add Task", font=("Arial", 12), command=add_task)
add_button.pack(pady=5)

# ปุ่มขีดฆ่า/คืนค่างาน
toggle_button = tk.Button(root, text="✔ Mark Done/Undo", font=("Arial", 12), command=toggle_task)
toggle_button.pack(pady=5)

# รายการงาน
listbox = tk.Listbox(root, font=("Arial", 12), height=15)
listbox.pack(pady=10, padx=10, fill=tk.BOTH)

# ปุ่มลบงาน
delete_button = tk.Button(root, text="❌ Delete Task", font=("Arial", 12), command=delete_task)
delete_button.pack(pady=5)

# แสดงรายการที่โหลดจากไฟล์
update_list()

# รัน GUI
root.mainloop()
