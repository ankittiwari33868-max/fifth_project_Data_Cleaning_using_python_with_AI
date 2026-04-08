# # Day 29
# GUI Based Automation using A.I 

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

# ------------------- FUNCTIONS -------------------

def browse_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx *.xls")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)

def browse_output_folder():
    folder_path = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, folder_path)

def reset_paths():
    input_entry.delete(0, tk.END)
    output_entry.delete(0, tk.END)

def reset_checkboxes():
    var_duplicates.set(0)
    var_blank.set(0)
    var_spaces.set(0)
    var_title.set(0)

def clean_data():
    input_file = input_entry.get()
    output_folder = output_entry.get()

    if not input_file or not output_folder:
        messagebox.showerror("Error", "Please select input file and output folder")
        return

    try:
        df = pd.read_excel(input_file)

        # -------- Apply Cleaning Options --------
        if var_duplicates.get():
            df = df.drop_duplicates()

        if var_blank.get():
            df = df.dropna(how='all')

        if var_spaces.get():
            text_cols = df.select_dtypes(include='object').columns
            df[text_cols] = df[text_cols].apply(lambda x: x.str.strip())

        if var_title.get():
            text_cols = df.select_dtypes(include='object').columns
            df[text_cols] = df[text_cols].apply(lambda x: x.str.title())

        # -------- Save File --------
        file_name = os.path.basename(input_file)
        output_file = os.path.join(output_folder, f"Cleaned_{file_name}")

        df.to_excel(output_file, index=False)

        messagebox.showinfo("Success", f"File cleaned and saved:\n{output_file}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ------------------- GUI SETUP -------------------

root = tk.Tk()
root.title("Data Cleaning Automation Tool")
root.geometry("500x400")

# Input File
tk.Label(root, text="Select Input Excel File").pack(pady=5)
input_entry = tk.Entry(root, width=50)
input_entry.pack()
tk.Button(root, text="Browse", command=browse_input_file).pack(pady=5)

# Output Folder
tk.Label(root, text="Select Output Folder").pack(pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.pack()
tk.Button(root, text="Browse", command=browse_output_folder).pack(pady=5)

# Checkboxes
tk.Label(root, text="Select Cleaning Options").pack(pady=10)

var_duplicates = tk.IntVar()
var_blank = tk.IntVar()
var_spaces = tk.IntVar()
var_title = tk.IntVar()

tk.Checkbutton(root, text="Remove Duplicate Rows", variable=var_duplicates).pack(anchor='w', padx=50)
tk.Checkbutton(root, text="Remove Blank Rows", variable=var_blank).pack(anchor='w', padx=50)
tk.Checkbutton(root, text="Trim Spaces (Text Columns)", variable=var_spaces).pack(anchor='w', padx=50)
tk.Checkbutton(root, text="Convert to Title Case (Text Columns)", variable=var_title).pack(anchor='w', padx=50)

# Buttons
tk.Button(root, text="Clean Data", bg="green", fg="white", command=clean_data).pack(pady=10)
tk.Button(root, text="Reset Paths", command=reset_paths).pack(pady=5)
tk.Button(root, text="Reset Checkboxes", command=reset_checkboxes).pack(pady=5)

root.mainloop()
