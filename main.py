import os
import sys
import tarfile
import tempfile
import zipfile

def initialize_filesystem(file):
    if not os.path.exists(file):
        print(f"File not found: {file}")
        sys.exit(1)
    if file.endswith(".tar"):
        return initialize_tar_filesystem(file)
    elif file.endswith(".zip"):
        return initialize_zip_filesystem(file)
    else:
        print(f"Unsupported file format: {file}")
        sys.exit(1)

def initialize_tar_filesystem(file):
    temp_dir = tempfile.mkdtemp()
    with tarfile.open(file, "r") as tar:
        tar.extractall(path=temp_dir)
    return temp_dir

def initialize_zip_filesystem(file):
    temp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(file, "r") as zip:
        zip.extractall(path=temp_dir)
    return temp_dir

def format_absolute_path(root_directory, current_directory):
    root_name = os.path.basename(root_directory)
    relative_path = os.path.relpath(current_directory, start=root_directory)
    if relative_path == ".":
        return "root:/"
    else:
        return f"root:/{relative_path}".replace("\\", "/")

def run_interactive_shell(file_system):
    root_directory = file_system
    current_directory = root_directory

    while True:
        try:
            absolute_path = format_absolute_path(root_directory, current_directory)
            user_input = input(f"{absolute_path}> ").strip()
            if user_input == "exit":
                break
            elif user_input == "pwd":
                print(absolute_path)
            elif user_input == "ls":
                files = os.listdir(current_directory)
                for file in files:
                    print(file)
            elif user_input.startswith("cd "):
                new_dir = user_input.split(" ", 1)[1]
                new_dir_path = os.path.join(current_directory, new_dir)
                if os.path.exists(new_dir_path) and os.path.isdir(new_dir_path):
                    current_directory = new_dir_path
                else:
                    print(f"Directory not found: {new_dir}")
            elif user_input.startswith("cat "):
                file_to_read = user_input.split(" ", 1)[1]
                file_path = os.path.join(current_directory, file_to_read)
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    with open(file_path, "r") as file:
                        print(file.read())
                else:
                    print(f"File not found: {file_to_read}")
            else:
                print(f"Command not found: {user_input}")
        except KeyboardInterrupt:
            print("\nExiting...")
            break

def execute_script(script_file, file_system):
    root_directory = file_system
    current_directory = root_directory
    with open(script_file, "r") as script:
        script_lines = script.readlines()
        for line in script_lines:
            absolute_path = format_absolute_path(root_directory, current_directory)
            user_input = line.strip()
            if user_input == "exit":
                break
            elif user_input == "pwd":
                print(absolute_path)
            elif user_input == "ls":
                files = os.listdir(current_directory)
                for file in files:
                    print(file)
            elif user_input.startswith("cd "):
                new_dir = user_input.split(" ", 1)[1]
                new_dir_path = os.path.join(current_directory, new_dir)
                if os.path.exists(new_dir_path) and os.path.isdir(new_dir_path):
                    current_directory = new_dir_path
                else:
                    print(f"Directory not found: {new_dir}")
            elif user_input.startswith("cat "):
                file_to_read = user_input.split(" ", 1)[1]
                file_path = os.path.join(current_directory, file_to_read)
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    with open(file_path, "r") as file:
                        print(file.read())
                else:
                    print(f"File not found: {file_to_read}")
            else:
                print(f"Command not found: {user_input}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <filesystem.tar|filesystem.zip> [--script <script.txt>]")
        sys.exit(1)

    file_system_file = sys.argv[1]
    file_system = initialize_filesystem(file_system_file)

    if "--script" in sys.argv:
        script_file_index = sys.argv.index("--script")
        if script_file_index + 1 < len(sys.argv):
            script_file = sys.argv[script_file_index + 1]
            execute_script(script_file, file_system)
    else:
        run_interactive_shell(file_system)
