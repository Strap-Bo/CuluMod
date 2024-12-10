import colorama
import sys
import const
import requests
import os
import webbrowser
import shutil
from time import sleep
import random
import wmi
import re
import subprocess

colorama.init(autoreset=True)

f = wmi.WMI()

flag = 0

print(f"{colorama.Fore.GREEN}Prepping...")

# clear
def clear():
    os.system('cls')

# sets the title
def set_title(newTitle):
    os.system(f'title CuluMod ^| {newTitle}')

# removes the ascii escape things that you would see in like txt compiled C,C#,C++ (i hate that )
def remove_ansi_escape_sequences(text):
    ansi_escape = re.compile(r'\x1b\[([0-9;]*)m') # i had to look on the internet on how to do this part btw.
    return ansi_escape.sub('', text)


# gets the version from the github
def get_version(cv):
    url = "https://raw.githubusercontent.com/Strap-Bo/CuluMod/main/Version.txt"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.text.strip()
        if cv == data:
            print(f"{colorama.Fore.GREEN}Running Culu5 {data}")
        else:
            print(f"{colorama.Fore.RED}Culu5 is not up to date! Going to the github to download the latest version. {data} -> {cv}")
            webbrowser.WindowsDefault('https://github.com/Strap-Bo/CuluMod/archive/refs/heads/main.zip')
    else:
        print(f"{colorama.Fore.RED}ERROR: Failed to retrieve the file. Status code: {response.status_code}")

# logs it to LogOutput.txt 
def log_output(message):
    clean_message = remove_ansi_escape_sequences(message) 
    with open("LogOutput.txt", "a", encoding="utf-8") as log_file:
        log_file.write(clean_message + "\n")
    print(message)


# opens a file
def open_file(filename):
    try:
        subprocess.Popen(f'explorer "{filename}"')
        print(f"{colorama.Fore.GREEN}Successfully opened {filename}")
    except Exception as e:
        print(f"{colorama.Fore.RED} ERROR: Directory {filename} does not exist.")

# silly animation
def ascii_animation(time, content):
    frames = ["|", "/", "-", "\\"]
    for _ in range(time):
        for frame in frames:
            sys.stdout.write(f"\r{colorama.Fore.BLUE}{content} {frame}")
            sys.stdout.flush()
            sleep(0.1)

def get_process():
    try:
        for process in f.Win32_Process():
            if "Gorilla Tag.exe" == process.name():
                log_output(f"{colorama.Fore.YELLOW}Gorilla tag is open... Closing gorilla tag")
                process.Terminate()
                flag = 1
                break
        if flag == 0:
            log_output(f"{colorama.Fore.GREEN}Gorilla tag is not open... Successfully running getGorilla()")
    except Exception as e:
        log_output(f"{colorama.Fore.RED}ERROR func,get_process() was left with a error: {e}")
            

# list files in directory function
def list_files_in_directory(directory):
    try:
        if os.path.exists(directory):

            log_output(f"\n{colorama.Fore.CYAN}Files in {directory}:")

            files = os.listdir(directory)
            if not files:
                log_output(f"{colorama.Fore.YELLOW}  (No files found in this directory)")
            else:
                for file in files:
                    file_path = os.path.join(directory, file)
                    if os.path.isfile(file_path):
                        file_type = "File"
                    else:
                        file_type = "Folder"
                    log_output(f"  - {file} ({file_type})")

    except Exception as e:
        log_output(f"{colorama.Fore.RED}Failed to list files in {directory}: {e}")

set_title("Prepping...")


# copy assets function
def copy_assets_to_oculus(assets_path, oculus_path, new_folder_name="Assets"):

    from utils import progress_bar

    destination_assets_path = os.path.join(oculus_path, new_folder_name)

    if os.path.exists(destination_assets_path):
        log_output(f"{colorama.Fore.YELLOW}Assets folder '{new_folder_name}' already exists at {destination_assets_path}. Files will be merged.")
    else:
        log_output(f"{colorama.Fore.GREEN}Creating '{new_folder_name}' folder at {destination_assets_path}...")
        os.makedirs(destination_assets_path)

    files_to_copy = []

    for root, dirs, files in os.walk(assets_path):
        for file in files:
            source_file = os.path.join(root, file)

            relative_path = os.path.relpath(source_file, assets_path)

            destination_file = os.path.join(destination_assets_path, relative_path)
            
            files_to_copy.append((source_file, destination_file))

    total_files = len(files_to_copy) # gets the amount not installed
    num_file = 0 # gets the amount installed

    if total_files == 0:
        log_output(f"{colorama.Fore.YELLOW}No files found in {assets_path} to install.")
        return
    
    for index, (source_file, destination_file) in enumerate(files_to_copy, start=1):
        os.makedirs(os.path.dirname(destination_file), exist_ok=True)
        
        shutil.copy2(source_file, destination_file)
        file_name = os.path.basename(source_file)

        clear()

        num_file+=1
        randomn = random.randint(1, 5)

        bar = progress_bar(index, total_files, f"Installing: {colorama.Fore.GREEN}{file_name}")
        ascii_animation(randomn, f"Installing {num_file}/{total_files}")
        set_title(f"Installed {num_file}/{total_files}")

    log_output(f"\n{colorama.Fore.GREEN}All files from '{assets_path}' have been successfully installed into '{destination_assets_path}'!")

# the main function
def getGorilla():
    try:
    # paths
        login = os.getlogin()
        assets_path = f"C:/Users/{login}/Downloads/culuMod/Assets/Culu5"
        oculus_path = "C:/Program Files/Oculus/Software/Software/another-axiom-gorilla-tag"
        bepinx_path = "C:/Program Files/Oculus/Software/Software/another-axiom-gorilla-tag/BepInEx"
        culumod_path = "C:/Program Files/Oculus/Software/Software/another-axiom-gorilla-tag/CuluMod"


        list_files_in_directory(bepinx_path)

        if os.path.exists(oculus_path):    
            if os.path.exists(bepinx_path):
                log_output(f"\n{colorama.Fore.RED}BepInEx folder already exists. Exiting...")
                sleep(5)
                os.system('exit')

        if os.path.exists(culumod_path):
            log_output(f"\n{colorama.Fore.YELLOW}CuluMod folder already exist! You don't need to do this unless there is a update.")

        get_version(cv="V0.1.2")
        get_process()
        ascii_animation(10, "Loading")
        copy_assets_to_oculus(assets_path, oculus_path, new_folder_name="CuluMod")
        open_file("C:\\Program Files\\Oculus\\Software\\Software\\another-axiom-gorilla-tag")
        set_title("Installed Assets!")
        os.system('pause Press any key to exit.')

    except Exception as e:
        print(f"{colorama.Fore.RED}FATAL ERROR: func,getGorilla() --exit")
        os.system('pause')
        os.system('exit')

if __name__ == "__main__":
    getGorilla()
