import os

source_folder = "C:/Users/kakad/Desktop/test"
files: list[str] = []

for file in os.listdir(source_folder):
    path = os.path.join(source_folder, file)
    if os.path.isfile(path):
        files.append(path)

sorted_list = sorted(files, key=os.path.getmtime)

def rename_files(new_name, extension=None):
    for i, source_file in enumerate(sorted_list, start=1):
        old_ext = os.path.splitext(source_file)[1]
        if extension is None:
            final_ext = old_ext
        else:
            final_ext = "." + extension
        new_filename = new_name + str(i) + final_ext
        new_path = os.path.join(source_folder, new_filename)
        os.rename(source_file, new_path)

rename_files("makima")
print(files)