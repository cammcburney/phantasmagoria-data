import os
from pathlib import Path
import shutil
from dotenv import load_dotenv
import time
import subprocess
import threading

stop_process = False

def load_env_variables():
    try:
        load_dotenv()

        source_directory = os.getenv('source_dir')
        destination_directory = os.getenv('destination_dir')

        return {"src_dir": source_directory, 
                "dest_dir": destination_directory}
    except Exception:
        print("Failed to source environment variables")


def get_files_in_directory(variable):
    try:
        return [file for file in os.listdir(variable) if type(dir) or file.endswith('.md')]
    except Exception:
        print("Failed to lookup files in directory")


def compare_files():
    try:
        variables = load_env_variables()
        src_files = get_files_in_directory(variables["src_dir"])
        dest_files = get_files_in_directory(variables["dest_dir"])
        src_to_copy = []
        for file in src_files:
            if not file.endswith('.md') and file != ".obsidian":
                src_to_copy.append(file)
        
        files_to_copy = set(src_files) - set(dest_files)
        set_ftc = set(src_to_copy)
        set_to_copy = files_to_copy | set_ftc
        return list(set_to_copy), variables["src_dir"], variables["dest_dir"]
    except Exception:
        print("Failed to compare files, please check paths and directories are not empty")

       

def copy_selected_files_to_folder():
    try:
        files, source, destination = compare_files()
        num = len(files)
        for file in files:
            
            src_path = os.path.join(source, file)
            dest_path = os.path.join(destination, file)
            if os.path.isdir(src_path):
                if not os.path.exists(dest_path):
                    shutil.copytree(src_path, dest_path)
            elif file.endswith('.md'):
                shutil.copy2(src_path, dest_path)
            elif file == ".obsidian":
                pass
        return num
    except Exception:
        print("Failed to new copy files")


def update_data_in_files(recursive_file=False, list_dirs=None):
    try:
        list_updated = []
        if list_dirs is None:
            list_dirs = []

        variables = load_env_variables()

        src_files = get_files_in_directory(variables["src_dir"])
        dest_files = get_files_in_directory(variables["dest_dir"])

        if recursive_file:
            dir_count = 0
            for dir in list_dirs:
                    if dir in list_dirs and dir != ".obsidian":
                        src_files = get_files_in_directory(f"{variables["src_dir"]}/{list_dirs[dir_count]}")
                        dest_files = get_files_in_directory(f"{variables["dest_dir"]}/{list_dirs[dir_count]}")
                        
                        for file in src_files:
                            src_path = os.path.join(f"{variables["src_dir"]}/{list_dirs[dir_count]}/", file)
                            dest_path = os.path.join(f"{variables["dest_dir"]}/{list_dirs[dir_count]}/", file)
                            with open(src_path, "r", encoding="utf-8") as src_file:
                                src_content = src_file.read()
                            with open(dest_path, "r", encoding="utf-8") as dest_file:
                                dest_content = dest_file.read()

                            if src_content != dest_content:
                                with open(dest_path, "w", encoding="utf-8") as dest_file:
                                    dest_file.write(src_content)
                                list_updated.append(file)
                        dir_count += 1
            list_dirs=[]
                
        else:
            for file in src_files:
                src_path = os.path.join(variables["src_dir"], file)
                dest_path = os.path.join(variables["dest_dir"], file)
                if os.path.isdir(src_path):
                    if file != ".obsidian":
                        list_dirs.append(file)
                elif file in dest_files:
                    with open(src_path, "r", encoding="utf-8") as src_file:
                        src_content = src_file.read()
                    with open(dest_path, "r", encoding="utf-8") as dest_file:
                        dest_content = dest_file.read()

                    if src_content != dest_content:
                        with open(dest_path, "w", encoding="utf-8") as dest_file:
                            dest_file.write(src_content)
                        list_updated.append(file)
        if len(list_dirs) > 0:
            update_data_in_files(recursive_file=True, list_dirs=list_dirs)
        
        return len(list_updated)
            
    except Exception:
        print("Failed to update files")

def delete_files_auto():
    try:
        list_updated = []
        variables = load_env_variables()
        src_files = get_files_in_directory(variables["src_dir"])
        dest_files = get_files_in_directory(variables["dest_dir"])

        for file in dest_files:
            dest_path = os.path.join(variables["dest_dir"], file)
            if file not in src_files:
                os.remove(dest_path)
                list_updated.append(file)

        return list_updated

    except Exception:
        print("Failed to delete files") 

def add_to_github(user_input, tc, tu, td):
    try:
        if user_input == "Y":
            current_dir = os.getcwd()
            
            os.chdir(os.path.join(current_dir, "..", ".."))

            subprocess.run(["git", "add", "."], check=True)
            
            cm = f"New files add to POD1 {tc} copied, {tu} updated and {td} deleted successfully!"
            subprocess.run(["git", "commit", "-m", cm], check=True)
            
            subprocess.run(["git", "push"], check=True)
            print("Phantasmagoria Obsidian Data sucessfully updated")
        else:
            print("No changes made to POD repository")

    except subprocess.CalledProcessError:
        print(f"An error occurred trying to push to Github")
