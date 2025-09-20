import os
import requests
import zipfile
import shutil
import time

# GitHub repo ZIP link
REPO_URL = "https://github.com/sepi12778/SEPEHR-CONFIG-/archive/refs/heads/main.zip"

# CODM data paths (MT Manager terminal)
CODM_BASE = "/storage/emulated/0/Android/data/com.activision.callofduty.shooter/files"
CODM_PATH_MAIN = os.path.join(CODM_BASE, "SEPEHR-CONFIG")
CODM_PATH_CONFIG = os.path.join(CODM_BASE, "config")

# Temp download/extract
TEMP_ZIP = "/storage/emulated/0/Download/sepehr_config.zip"
EXTRACT_PATH = "/storage/emulated/0/Download/sepehr_config"

# ANSI color codes
YELLOW = "\033[93m"
GREEN = "\033[92m"
CYAN = "\033[96m"
RED = "\033[91m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# Simple loader
def loader(text="Processing"):
    for i in range(3):
        print(f"\r{YELLOW}{text}{'.'*i}  {RESET}", end="", flush=True)
        time.sleep(0.5)
    print("\r", end="")

def download_repo():
    print(f"{YELLOW}[*] Downloading repository from GitHub...{RESET}")
    r = requests.get(REPO_URL)
    with open(TEMP_ZIP, "wb") as f:
        f.write(r.content)
    loader("Extracting files")
    with zipfile.ZipFile(TEMP_ZIP, "r") as zip_ref:
        zip_ref.extractall(EXTRACT_PATH)
    print(f"{GREEN}[✓] Download and extraction complete!{RESET}\n")

def copy_files(source, target):
    if not os.path.exists(target):
        os.makedirs(target)
    for item in os.listdir(source):
        s = os.path.join(source, item)
        d = os.path.join(target, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

def activate():
    download_repo()
    repo_folder = os.path.join(EXTRACT_PATH, "SEPEHR-CONFIG--main")

    print(f"{CYAN}[*] Copying to main folder...{RESET}")
    copy_files(repo_folder, CODM_PATH_MAIN)
    print(f"{GREEN}[✓] Files copied to main folder{RESET}")

    print(f"{CYAN}[*] Copying to config folder...{RESET}")
    copy_files(repo_folder, CODM_PATH_CONFIG)
    print(f"{GREEN}[✓] Files copied to config folder{RESET}\n")

def deactivate():
    print(f"{RED}[*] Removing CODM configuration...{RESET}")
    for path in [CODM_PATH_MAIN, CODM_PATH_CONFIG]:
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"{GREEN}[✓] Removed: {path}{RESET}")
        else:
            print(f"{YELLOW}[!] Not found: {path}{RESET}")
    print("")

def main_menu():
    while True:
        print(f"{MAGENTA}\n=== SEPEHR CODM Mini App ==={RESET}")
        print(f"{CYAN}1. Toggle CODM Config (ON/OFF){RESET}")
        print(f"{CYAN}2. Exit{RESET}")
        choice = input("Enter your choice: ")

        if choice == "1":
            if os.path.exists(CODM_PATH_MAIN) or os.path.exists(CODM_PATH_CONFIG):
                deactivate()
            else:
                activate()
        elif choice == "2":
            print(f"{GREEN}Exiting... Goodbye 👋{RESET}")
            break
        else:
            print(f"{RED}Invalid choice, try again!{RESET}")

if __name__ == "__main__":
    main_menu()
