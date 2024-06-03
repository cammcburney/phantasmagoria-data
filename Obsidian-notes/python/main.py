import os
from pathlib import Path
import shutil
from dotenv import load_dotenv
import time
import subprocess
import threading
from utils import *

def monitor_user_input():
    global stop_process
    while True:
        user_input = input()
        if user_input.lower() == 'x':
            stop_process = True
            break

def monitor_file_changes_to_invoke_function():
    total_copied = 0
    total_updated = 0 
    total_deleted = 0
    list_of_deleted_files = []

    user_input_thread = threading.Thread(target=monitor_user_input)
    user_input_thread.daemon = True
    user_input_thread.start()

    try:
        while stop_process is False:
            print("Active and checking for new data ≽^•⩊•^≼ input x to exit...")
            files_copied = copy_selected_files_to_folder()
            if files_copied > 0:
                print(f"{files_copied} new files copied ദ്ദി ˉ͈̀꒳ˉ͈́ )✧")
                total_copied += files_copied

            num_updated = update_data_in_files()
            if num_updated > 0:
                print(f"{num_updated} files updated ٩(ˊᗜˋ*)و ♡")
                total_updated += num_updated
            
            deleted_files = delete_files_auto()
            if len(deleted_files) > 0:
                print(f"{len(deleted_files)} files deleted ≽^╥⩊╥^≼")
                total_deleted += len(deleted_files)
                for df in deleted_files:
                    list_of_deleted_files.append(df)

            print("Resting... /ᐠ - ˕ -マᶻ 𝗓 𐰁")
            for _ in range(60):
                if stop_process:
                    break
                time.sleep(1) 
            
            
    except Exception:
        print("An error occured while running the program")

    finally:
        print("File copy operation shut down")
        print("Summary:")
        print(f"{total_copied} new files copied")
        print(f"{total_updated} files updated")
        print(f"{total_deleted} files deleted")
        if total_deleted > 0:
            for del_file in list_of_deleted_files:
                print(f"{del_file} deleted")

        user_input = input("Commit changes to POD repository? Y/N : ")
        add_to_github(user_input, tc=total_copied, tu=total_updated, td=total_deleted)

if __name__ == "__main__":
    monitor_file_changes_to_invoke_function()
