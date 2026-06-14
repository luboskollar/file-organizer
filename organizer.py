import os
import shutil
import tkinter as tk
from tkinter import filedialog
from PIL import Image


def get_files():
    files: list[str] = []
    for file in os.listdir(source_folder):
        path = os.path.join(source_folder, file)
        if os.path.isfile(path):
            files.append(path)
    sorted_list = sorted(files, key=os.path.getmtime)
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

def get_folder():
    global source_folder
    source_folder = filedialog.askdirectory()
    print(source_folder)

def run():
    files = get_files()
    process_files(files, new_name="makima", extension="jpg", copy=True)

window = tk.Tk()
window.title("Organizer")

label = tk.Label(window, text="Ahoj")
label.pack()

button_choose = tk.Button(window, text="Choose folder", command=get_folder)
button_choose.pack()

button_run = tk.Button(window, text="Run", command=run)
button_run.pack()

window.mainloop()
