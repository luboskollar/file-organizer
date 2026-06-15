# ===================== IMPORTS =====================
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image

# ===================== LOGIC =====================
source_folder = ""
def get_files():
    files: list[str] = []
    for file in os.listdir(source_folder):
        path = os.path.join(source_folder, file)
        if os.path.isfile(path):
            files.append(path)
    choice = sort_choice.get()
    if choice == "created":
        sorted_list = sorted(files, key=os.path.getctime)
    else:
        sorted_list = sorted(files, key=os.path.basename)
    return sorted_list

def process_files(sorted_list, new_name, extension=None, copy=False):
    for i, source_file in enumerate(sorted_list, start=1):
        old_ext = os.path.splitext(source_file)[1]
        if extension is None:
            final_ext = old_ext
        else:
            final_ext = "." + extension
        new_filename = new_name + str(i) + final_ext
        new_path = os.path.join(source_folder, new_filename)
        if final_ext == ".jpg" and old_ext != ".jpg":
            # Real format conversion (e.g. PNG -> JPG) using Pillow.
            # This strips metadata (e.g. AI generation prompts) and recompresses.
            # Original file is always kept, regardless of `copy` parameter.
            img = Image.open(source_file)
            img.convert("RGB").save(new_path, quality=100)
        else:
            # No format change - just rename or copy with new filename
            if copy:
                shutil.copy(source_file, new_path)
            else:
                os.rename(source_file, new_path)

# ===================== GUI CALLBACKS =====================
def get_folder():
    global source_folder
    source_folder = filedialog.askdirectory()
    parts = source_folder.split("/")
    if len(parts) > 3:
        display_path = "..." + "/".join(parts[-3:])
    else:
        display_path = source_folder

    label_path.configure(text=display_path)

def run():
    files = get_files()
    copy = copy_var.get()
    if convert_var.get():
        extension = "jpg"
    else:
        extension = None
    try:
        process_files(files, new_name=entry_name.get(), extension=extension, copy=copy)
        messagebox.showinfo("Success", "Files successfully processed")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ===================== GUI SETUP =====================
window = ctk.CTk()
window.title("Organizer")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
# ===================== GUI WIDGETS =====================
label_path = ctk.CTkLabel(window, text="No folder selected", width=10, anchor="w")
label_path.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="we")

button_choose = ctk.CTkButton(window, text="Choose folder", command=get_folder, width=200)
button_choose.grid(row=0, column=1, padx=10, pady=5)

button_run = ctk.CTkButton(window, text="Run", command=run, width=100)
button_run.grid(row=5, column=2, sticky="e", padx=5, pady=10)

label_name = ctk.CTkLabel(window, text="Entry name")
label_name.grid(row=1, column=0, sticky="w", padx=5)

entry_name = ctk.CTkEntry(window, width=200)
entry_name.grid(row=1, column=1, padx=5)

label_sort = ctk.CTkLabel(window, text="Sort by:")
label_sort.grid(row=0, column=2, sticky="w", padx=5)

sort_choice = tk.StringVar(value="created")
radio_created = ctk.CTkRadioButton(window, text="Created", variable=sort_choice, value="created")
radio_created.grid(row=1, column=2, sticky="w", padx=5)

radio_name = ctk.CTkRadioButton(window, text="Name", variable=sort_choice, value="name")
radio_name.grid(row=2, column=2, sticky="w", padx=5)

copy_var = tk.BooleanVar(value=False)
check_copy = ctk.CTkCheckBox(window, text="Copy (keep originals)", variable=copy_var)
check_copy.grid(row=4, column=0, sticky="w", padx=5)

convert_var = tk.BooleanVar(value=False)
check_convert = ctk.CTkCheckBox(window, text="Convert PNG to JPG (this copies files by default)", variable=convert_var)
check_convert.grid(row=4, column=1, sticky="w", padx=5)

window.mainloop()
