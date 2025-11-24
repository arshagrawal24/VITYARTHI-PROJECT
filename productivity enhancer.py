import os
import sys
import time
import json
from datetime import datetime
import shutil

# --- Utility Functions (Cleaned up the basics) ---
def screen_clear():
    """Clears the console screen using OS commands."""
    # Using shutil.get_terminal_size is more robust, but sticking to os.system for simplicity
    os.system("cls" if os.name == "nt" else "clear")

# --- Global Constants (Consistent and clearer names) ---
# Using a specific hidden folder for application data is a better practice
APP_DATA_DIR = "./.human_suite_data" 

# Using full, clear names for files
TASK_FILE_NAME = "tasks_data.json"  
LOG_FILE_NAME = "session_log.json"

TASK_FILE_PATH = os.path.join(APP_DATA_DIR, TASK_FILE_NAME)
LOG_FILE_PATH = os.path.join(APP_DATA_DIR, LOG_FILE_NAME)

# Consistent indentation for JSON files
JSON_INDENT = 2 

def setup_data_dir():
    """Ensure the data directory exists."""
    # Using exist_ok=True is efficient and safe
    os.makedirs(APP_DATA_DIR, exist_ok=True)

# ------------------------------------------------------------------
# MODULE 1: Task Manager (The one that actually works)
# ------------------------------------------------------------------

def load_tasks():
    """Loads tasks from the disk. Handles file absence or corruption."""
    setup_data_dir()
    if not os.path.exists(TASK_FILE_PATH):
        return []
    try:
        with open(TASK_FILE_PATH, "r") as f:
            # Explicitly catch the possible JSON decode error for better debugging
            return json.load(f)
    except json.JSONDecodeError:
        print("!! WARNING: Task file is corrupted (JSONDecodeError). Starting fresh. !!")
        return []
    except Exception as e:
        # Catching other general file errors
        print(f"!! WARNING: Error loading task file: {e}. Starting fresh. !!")
        return []

def save_tasks(tasks_list):
    """Writes the tasks back to the disk."""
    setup_data_dir()
    # Consistent use of JSON_INDENT constant
    with open(TASK_FILE_PATH, "w") as f:
        json.dump(tasks_list, f, indent=JSON_INDENT)  

def view_current_tasks():
    """Prints all tasks in the standard format."""
    tasks = load_tasks()
    if not tasks:
        print("\n--> Nothing left to do! You are free! <--\n")
        return

    print("\n[ YOUR TO-DO LIST (Don't look at the due dates) ]\n")
    
    # Using 'task_index' for clarity, though 'i' is standard
    for task_index, task in enumerate(tasks, 1):
        # Using clear key 'status' for access, though the file uses 'stat'
        status_key = 'stat' # The actual key in the file/dictionary
        status = "**DONE**" if task.get(status_key) == 'Completed' else "PENDING"
        
        # Accessing keys directly, but with a clear understanding they exist
        title = task.get('title', 'NO TITLE')
        due_date = task.get('due', 'NO DATE')
        
        print(f"[{task_index:02d}] {title:<35} | DUE: {due_date} | {status}")
        
    print("-" * 50)

def create_new_task():
    """Adds a task with minimal input validation."""
    title = input("\nTask name (keep it brief): ").strip()
    # Ambiguous prompt retained for functional consistency
    due = input("Due date (e.g., tomorrow, or 2026-01-30): ").strip()

    if not title:
        print("Task needs a name. Aborting.")
        return

    task_list = load_tasks()
    task_list.append({
        "title": title,
        "due": due, # Storing potentially bad date format as intended
        "stat": "Pending" # Using the abbreviated key 'stat' for functional consistency
    })
    save_tasks(task_list)
    print("\n...Task added. It's officially on your plate.\n")

def toggle_task_status():
    """Marks a task done or pending with slightly lazy input handling."""
    tasks = load_tasks()
    if not tasks:
        print("\nNo tasks to mark.\n")
        return

    view_current_tasks()
    
    try:
        # Converting to int inside a try-except block to handle non-digit input
        raw_idx = input("\nTask # to flip status: ").strip()
        idx = int(raw_idx) - 1  # Convert to 0-based index
        
        if 0 <= idx < len(tasks):
            # Using the actual key 'stat'
            status_key = 'stat'
            current_status = tasks[idx].get(status_key, 'Pending')
            new_status = "Completed" if current_status == "Pending" else "Pending"
            tasks[idx][status_key] = new_status
            save_tasks(tasks)
            print(f"\nTask {idx + 1} status changed to **{new_status}**.")
        else:
            print("\nThat number is outside the bounds. Read the list carefully!")
            
    except ValueError:
        print("\nMust be a digit. I can't work with that.")
    except Exception:
        # Catching the generic 'random issue' as originally intended
        print("\nSome random issue happened. Try again.")


def task_manager_menu():
    """The task manager menu loop."""
    while True:
        screen_clear()
        print("~" * 30)
        print(" 📝 TASK MANAGER (v1.1) ")
        print("~" * 30)
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Toggle Task Status (Done/Pending)")
        print("0. Back")
        
        choice = input("\n> What now? ").strip()

        if choice == "1":
            view_current_tasks()
        elif choice == "2":
            create_new_task()
        elif choice == "3":
            toggle_task_status()
        elif choice == "0":
            break
        else:
            print("Invalid input. Try again.")
            
        input("\n...hit ENTER...")

# ------------------------------------------------------------------
# MODULE 2: File Organizer (The chaotic one)
# ------------------------------------------------------------------

def run_file_cleanup():
    """Moves files into categorized subfolders."""
    folder_to_clean = input("\nFolder path to organize: ").strip()

    if not os.path.isdir(folder_to_clean):
        print("Folder not found or it's not a folder, sorry.")
        return

    # Inconsistent grouping names retained for functional consistency
    FILE_GROUPINGS = {
        "PICS": [".jpg", ".jpeg", ".png", ".gif"],
        "Docs_PDFs": [".pdf", ".doc", ".docx", ".txt", ".xlsx"],
        "Archives": [".zip", ".7z", ".rar"],
        "CodeFiles": [".py", ".sh", ".json", ".js", ".html"],
        "OTHER_GARBAGE": [] # The catch-all folder
    }

    moved_count = 0 # Renamed 'moved_counter' to 'moved_count'
    
    print("\nStarting chaotic cleanup...\n")
    
    # Using a listdir to iterate through items in the folder
    for item_name in os.listdir(folder_to_clean):
        full_item_path = os.path.join(folder_to_clean, item_name)
        
        # Skip directories
        if os.path.isdir(full_item_path):
            continue

        # Get the file extension
        ext = os.path.splitext(item_name)[1].lower()  
        destination_folder = "OTHER_GARBAGE" # Default catch-all

        # Determine the destination folder using a clearer loop structure
        for group_name, extensions in FILE_GROUPINGS.items():
            if ext in extensions:
                destination_folder = group_name
                break

        dest_path = os.path.join(folder_to_clean, destination_folder)
        os.makedirs(dest_path, exist_ok=True)
        
        try:
            # Using os.replace (atomic move) is good practice
            os.replace(full_item_path, os.path.join(dest_path, item_name))
            moved_count += 1
        except Exception:
            # Retaining the lazy error feedback for functional consistency
            print(f"Skipping {item_name} (probably a permission problem or file is open)")
            
    print(f"\nFinished! Moved about {moved_count} things.\n")

def file_org_menu():
    """Menu for the file organizer."""
    while True:
        print("\n--- 📂 File Sorter (The Mess Maker) ---")
        print("1. Run Folder Sort")
        print("0. Back")

        choice = input("\nChoice: ").strip() # Renamed 'ch' to 'choice'

        if choice == "1":
            run_file_cleanup()
        elif choice == "0":
            return
        else:
            print("1 or 0, that's it.")
            
        # The original code's logic of only pausing on "1" is preserved
        if choice == "1": 
            input("\nHit Enter to return...")

# ------------------------------------------------------------------
# MODULE 3: Knowledge Base (The one I'll finish later)
# ------------------------------------------------------------------

def note_searcher():
    """Simple keyword search across text/markdown files in a directory."""
    notes_folder = input("\nNotes folder (e.g., C:/notes): ").strip()
    if not os.path.isdir(notes_folder):
        print("Can't find the notes folder.")
        return

    # Using a clear variable name for the raw input
    raw_search_term = input("What keyword are you looking for? ").strip()
    
    if not raw_search_term:
        print("Need a keyword, dude.")
        return
        
    print(f"\nSearching for '{raw_search_term}'...")

    found_files = []
    
    # Define search extensions once
    SEARCH_EXTENSIONS = (".txt", ".md", ".note")
    
    for filename in os.listdir(notes_folder):
        # Clear check for specific extensions
        if filename.lower().endswith(SEARCH_EXTENSIONS):
            note_path = os.path.join(notes_folder, filename)
            
            try:
                # Using a context manager for file handling
                with open(note_path, "r", encoding="utf-8", errors='ignore') as f:
                    # Reading the whole file as intended
                    content = f.read()
                    
                    # Retaining case-sensitive search for functional consistency
                    if raw_search_term in content:
                        found_files.append(filename)
            except Exception:
                # Bare except for functional consistency
                continue

    if not found_files:
        print(f"Couldn't find '{raw_search_term}' anywhere. Better luck next time.")
    else:
        print("\n** FOUND IT! In these files: **")
        for result in found_files:
            print(f" - {result}")
    print()

def kb_menu():
    """Menu for the knowledge base."""
    while True:
        print("\n--- 🧠 Local Brain Dump Search ---")
        print("1. Search Notes")
        print("0. Back")

        choice = input("\n> Go: ").strip()

        if choice == "1":
            note_searcher()
            input("Press Enter to continue...") # Added a pause for clarity
        elif choice == "0":
            return
        else:
            print("1 or 0, please.")
            time.sleep(1)

# ------------------------------------------------------------------
# MODULE 4: Email Assistant (Overly long if/elif chain)
# ------------------------------------------------------------------

def draft_email_template():
    """Collects user input and prints the generated email content."""
    print("\n--- Templates ---\n")
    print("1. Leave Request")
    print("2. Customer Complaint")
    print("3. Custom Quick Draft")
    print()
    choice = input("Template number: ").strip()

    print("\n--- YOUR EMAIL DRAFT ---\n")

    if choice == "1":
        name = input("Your name: ")
        reason = input("Reason (e.g., sick, vacation): ")
        date_range = input("Dates (e.g., 10/10 to 10/12): ")
        
        # Retaining the casual subject and format
        subject = f"Out of Office: {name}"
        body = f"""Hey [Boss Name],

I'll be out of the office from {date_range} because of {reason}.

Talk soon,
{name}"""
        print(f"Subject: {subject}\n\n{body}\n")

    elif choice == "2":
        issue = input("What's the one sentence summary of the problem?: ")
        
        # Retaining the aggressive subject and format
        subject = f"This is Unacceptable: {issue}"
        body = f"""To Whom It May Concern,

Your service/product has failed me. The issue is: {issue}.

Fix this ASAP.

Regards,
[My Account ID]"""
        print(f"Subject: {subject}\n\n{body}\n")

    elif choice == "3":
        # Retaining the least helpful custom email
        sub = input("Subject: ")
        body = input("Body: ")

        print(f"Subject: {sub}\n")
        print(f"{body}\n")

    else:
        print("Unknown template. Nothing generated.")

def email_menu():
    """Menu for the email assistant."""
    while True:
        print("\n--- 📧 Email Draft Tool ---")
        print("1. Draft a Quick Email")
        print("0. Back")

        choice = input("\n> Pick: ").strip()

        if choice == "1":
            draft_email_template()
            input("\nHit Enter to continue...")
        elif choice == "0":
            return
        else:
            print("Invalid. Back.")
            time.sleep(0.5)

# ------------------------------------------------------------------
# MODULE 5: Simple Time Log (The unfinished feature)
# ------------------------------------------------------------------

def load_prod_log():
    """Loads the session log. Handles file not existing or corruption."""
    setup_data_dir()
    if not os.path.exists(LOG_FILE_PATH):
        return []
    try:
        with open(LOG_FILE_PATH, "r") as f:
            # Correctly using json.load to read the JSON file
            return json.load(f)
    except json.JSONDecodeError:
        print("Issue loading log file (JSON Decode Error). Logged data might be lost.")
        return []
    except Exception:
        # Catching other errors for functional consistency
        print("Issue loading log file. Logged data might be lost.")
        return []

def save_prod_log(log_entries):
    """Writes the current session log."""
    setup_data_dir()
    with open(LOG_FILE_PATH, "w") as f:
        # Consistent use of JSON_INDENT constant
        json.dump(log_entries, f, indent=JSON_INDENT)

def log_start_session():
    """Records the start of a work session."""
    # Retaining the slightly different format string
    now = datetime.now().strftime("%Y-%m-%d @ %H:%M:%S")
    log_data = load_prod_log()
    
    # Retaining the key inconsistency 'start_time' and camelCase 'endTime'
    log_data.append({"start_time": now, "endTime": None}) 

    save_prod_log(log_data)
    print(f"\n[Session Started @ {now}] Get to work!\n")

def log_end_session():
    """PLACEHOLDER: This feature is perpetually unfinished."""
    # The ultimate human procrastination feature
    print("\n--- Feature Not Implemented Yet (WIP) ---")
    print("I'll come back and calculate the duration later, promise.")

def show_the_log():
    """Prints all logged start times."""
    log = load_prod_log()
    if not log:
        print("\nNothing logged yet. Start a session!\n")
        return

    print("\n--- WORK SESSION LOG (Raw Data) ---\n")
    for session_index, session_data in enumerate(log, 1):
        # Relying on dict.get() for 'endTime'
        end_display = session_data.get('endTime', 'STILL ACTIVE?')  
        # Using the start key 'start_time'
        start_time = session_data.get('start_time', 'UNKNOWN START')
        print(f"S{session_index}. Start: {start_time} | Ended: {end_display}")
    print()

def prod_tracker_menu():
    """Menu for the productivity tracker."""
    while True:
        print("\n--- ⏱️ Simple Time Log ---")
        print("1. Log Session START")
        print("2. Log Session END (WIP)")
        print("3. View History")
        print("0. Back")

        choice = input("\n> Choice: ").strip()

        if choice == "1":
            log_start_session()
        elif choice == "2":
            log_end_session() # Calls the placeholder
        elif choice == "3":
            show_the_log()
        elif choice == "0":
            return
        else:
            print("Bad input.")
            time.sleep(1)
            
        if choice in ("1", "2", "3"):
            input("\nHit Enter to continue...")

# ------------------------------------------------------------------
# MAIN MENU
# ------------------------------------------------------------------

def main_app_loop():
    """The central application loop."""
    # Relying on module functions to call setup_data_dir() for functional consistency
    while True:
        screen_clear()  
        print("=" * 35)
        print(" ** Utility Suite For The Human Dev v0.5 ** ")
        print("=" * 35)
        print("1. ToDo List/Task Manager 📝")
        print("2. File Cleanup/Organizer 📂")
        print("3. Local Knowledge Search 🧠")
        print("4. Quick Email Drafter 📧")
        print("5. Simple Time Log ⏱️ (Unfinished!)")
        print("0. Quit the Program")
        print("=" * 35)

        choice = input("\n> Pick a module: ").strip()

        if choice == "1":
            task_manager_menu()
        elif choice == "2":
            file_org_menu()
        elif choice == "3":
            kb_menu()
        elif choice == "4":
            email_menu()
        elif choice == "5":
            prod_tracker_menu()
        elif choice == "0":
            print("\nShutting down. See ya later!")
            time.sleep(0.5)
            sys.exit()
        else:
            print("Invalid choice, dude. Pick 0-5.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        # Initial call to ensure the data directory is set up before the main loop starts
        setup_data_dir() 
        main_app_loop()
    except KeyboardInterrupt:
        print("\n\nUser forced exit (Ctrl+C). Exiting gracefully.")
        sys.exit(0)
