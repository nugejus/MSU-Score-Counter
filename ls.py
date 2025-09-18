import os

def print_files_recursively(directory_path):
    """
    Prints the full path of all files within a given directory
    and its subdirectories.
    """
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if "venv" not in file_path and "pycache" not in file_path:
                print(file_path)

print_files_recursively('.')