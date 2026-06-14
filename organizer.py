# ===================== IMPORTS =====================
import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
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
    print(source_folder)

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
window = tk.Tk()
window.title("Organizer")

# ===================== GUI WIDGETS =====================
button_choose = tk.Button(window, text="Choose folder", command=get_folder)
button_choose.pack()

button_run = tk.Button(window, text="Run", command=run)
button_run.pack()

label_name = tk.Label(window, text="Entry name")
label_name.pack()

entry_name = tk.Entry(window, width=30)
entry_name.pack()

sort_choice = tk.StringVar(value="created")
radio_created = tk.Radiobutton(window, text="Created", variable=sort_choice, value="created")
radio_created.pack()

radio_name = tk.Radiobutton(window, text="Name", variable=sort_choice, value="name")
radio_name.pack()

copy_var = tk.BooleanVar(value=False)
check_copy = tk.Checkbutton(window, text="Copy (keep originals)", variable=copy_var)
check_copy.pack()

convert_var = tk.BooleanVar(value=False)
check_convert = tk.Checkbutton(window, text="Convert PNG to JPG (this copies files by default)", variable=convert_var)
check_convert.pack()

window.mainloop()
