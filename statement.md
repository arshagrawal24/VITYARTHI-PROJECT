# Project Statement: The Utility Suite For The Human Dev v0.5

## 1. Project Overview

The Utility Suite For The Human Dev v0.5 (HUS v0.5) is a lightweight,
cross-platform command-line interface (CLI) application built in Python.
Its primary purpose is to address the cognitive load and inefficiency
associated with task fragmentation by consolidating essential, routine
personal productivity and administrative functions into a single,
cohesive tool. The suite prioritizes local data storage (via JSON files)
and simple, rapid execution to minimize context switching and maximize
the user's flow state.

## 2. Problem Addressed

Modern workflows require constant switching between distinct
applications for tasks (To-Do apps), organization (File
Explorer/Finder), information retrieval (Note Search), and communication
(Email client). This fragmentation creates bottlenecks, increases
context switching time, and disperses personal data across multiple
platforms.

## 3. Project Goals and Objectives

### Consolidation

Integrated five distinct utilities into a single, navigable console
interface.

### Data Integrity

Ensured persistent, local storage for task and time log data using
robust JSON handling.

### Workflow Efficiency

Provided rapid execution for common tasks, such as automated file
sorting and template drafting.

### Extensibility

Designed modules to be functionally separate and easily expandable,
specifically catering to the future expansion of the Time Log feature.

## 4. Scope and Deliverables

### Module 1: Task Manager

**Description:** Provides CRUD-lite operations for managing a persistent
to-do list (View, Add, Toggle Status).\
**Key Deliverable:** Reliable data persistence via the tasks_data.json
file.

### Module 2: File Organizer

**Description:** A utility to scan a user-specified directory and
automatically move files into extension-based, categorized subfolders.\
**Key Deliverable:** The fully implemented run_file_cleanup() function.

### Module 3: Knowledge Base Search

**Description:** A keyword search function across a user-defined
directory of text files (.txt, .md) to quickly locate personal notes.\
**Key Deliverable:** The fully implemented note_searcher() function.

### Module 4: Email Assistant

**Description:** A menu-driven system to collect minimal inputs and
output fully formatted, copy-paste-ready email templates (e.g., Leave
Request, Complaint).\
**Key Deliverable:** The draft_email_template() function.

### Module 5: Simple Time Log

**Description:** A foundational logging system for recording the start
time of work sessions.\
**Key Deliverable:** Data persistence via the session_log.json file.\
Note: The Log Session END functionality and duration calculation are
Work In Progress (WIP) and out of scope for the v0.5 delivery.

## 5. Technical Stack

-   **Language:** Python 3.x\
-   **Interface:** Command Line Interface (CLI)\
-   **Persistence:** JSON files stored in a local .human_suite_data
    directory\
-   **Libraries:** Standard library only (os, sys, time, json, datetime,
    shutil)

## 6. Success Metrics

The project is considered successful if: - All five modules (with Module
5's noted limitation) execute reliably without crashes. - Data integrity
is maintained (tasks and logs persist correctly between sessions). - The
CLI interface provides clear, user-friendly navigation for non-technical
users.
