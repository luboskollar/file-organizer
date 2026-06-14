import os

source_folder = "C:/Users/kakad/Desktop/test"
files = []

for file in os.listdir(source_folder):
    path = os.path.join(source_folder, file)
    if os.path.isfile(path):
        files.append(path)
print(files)
print(len(files))