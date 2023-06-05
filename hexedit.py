import tkinter as tk
from tkinter import filedialog, messagebox, Text
import os
import threading
import tempfile
import shutil

temp_file_path = ""

def load_file():
    filepath = filedialog.askopenfilename(initialdir="/", title="Select file")
    if filepath:
        file_path_label.config(text=filepath)
        threading.Thread(target=process_file, args=(filepath,)).start()

def process_file(filepath):
    global temp_file_path
    try:
        with open(filepath, 'rb') as f, tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name
            while chunk := f.read(8192):
                temp_file.write(chunk.hex().encode())
    except Exception as e:
        messagebox.showerror("Error", str(e))
    else:
        read_hex_file(temp_file_path)

def read_hex_file(filepath):
    hex_dump.delete('1.0', tk.END)
    try:
        with open(filepath, 'r') as f:
            hex_dump.insert(tk.END, f.read())
    except Exception as e:
        messagebox.showerror("Error", str(e))

def save_hex():
    global temp_file_path
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text file", "*.txt"), ("All Files", "*.*")))
    if filepath and temp_file_path:
        shutil.move(temp_file_path, filepath)
        temp_file_path = ""

root = tk.Tk()
root.title("Hex Dumper")

file_path_label = tk.Label(root, text="")
file_path_label.pack()

hex_dump = Text(root)
hex_dump.pack()

load_button = tk.Button(root, text="Load new file", command=load_file)
load_button.pack()

save_button = tk.Button(root, text="Dump hex to txt file", command=save_hex)
save_button.pack()

root.mainloop()
