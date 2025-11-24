# Utility Suite for the Human Dev

A lightweight command-line productivity toolkit built in Python. It
provides tools for task management, file organization, note searching,
email drafting, and simple time logging.

## Features

### Task Manager

-   Add, view, and toggle tasks.
-   Tasks stored in a JSON file.
-   Simple and terminal-friendly.

### File Organizer

-   Automatically sorts files into categorized subfolders.
-   Supports images, documents, archives, code files, and a catch‑all
    folder.
-   Skips locked or inaccessible files safely.

### Notes Searcher

-   Keyword search across .txt, .md, and .note files.
-   Case-sensitive search.

### Email Draft Assistant

-   Generates quick email drafts.
-   Includes templates for leave requests, customer complaints, and
    custom messages.

### Simple Time Log (WIP)

-   Logs session start times.
-   End-time tracking not implemented yet.
-   Logs stored in JSON.

## Installation

1.  Download or clone the repository from GitHub.
2.  Ensure Python 3.8 or newer is installed.
3.  No external dependencies are required.

## Usage

1.  Open your terminal or command prompt.
2.  Navigate to the project folder.
3.  Run the main file named "main.py".
4.  Use the on‑screen menu to select a module:
    -   Task Manager
    -   File Organizer
    -   Note Searcher
    -   Email Draft Tool
    -   Time Log
5.  Follow the prompts for each feature.
6.  Choose the quit option to exit the application.

## Data Storage

All saved data is stored in a folder named `.human_suite_data`, created
automatically at runtime.\
This folder contains: - tasks_data.json\
- session_log.json

## Requirements

-   Python 3.8 or newer
-   Works on Windows, macOS, and Linux

## License

MIT License (or any license you choose to include)
