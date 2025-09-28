# Python Log File Analyzer Suite ⚙️

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![Status](https://img.shields.io/badge/status-complete-green.svg)
![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)

This repository contains a suite of three Python scripts that demonstrate progressive levels of log file manipulation and analysis. The projects showcase core Python skills in file I/O, string manipulation, and data processing.

---
## Projects Overview

This suite contains three milestones, each demonstrating a different aspect of log file processing. Click on a milestone to see its details.

<details>
<summary><strong>Milestone 1: Log File Editor & Counter</strong></summary>

### Task
This script functions as a basic log file editor. It reads an initial log file and a command file, then applies **`REPLACE`** commands to modify the content of specific lines in the log.

-   **Input:** A log file with various system events and a command file with `REPLACE` instructions.
-   **Output:** A new, processed log file with the modifications applied, and a summary file counting the total number of `INFO`, `WARN`, and `ERROR` messages.

</details>

<details>
<summary><strong>Milestone 2: Advanced Log Editor & User Analyzer</strong></summary>

### Task
This is an advanced version of the editor that processes **`DELETE`** and **`INSERT`** commands to remove or add entire lines to a log file. After editing, it performs a specific analysis to extract user activity data.

-   **Input:** A log file and a command file with `DELETE` and `INSERT` instructions.
-   **Output:** A processed log file with lines added/removed, and a summary file that counts how many times each unique user has logged in.

</details>

<details>
<summary><strong>Milestone 3: Log File "Diff" Generator</strong></summary>

### Task
This script performs the reverse of the first two milestones. It takes two log files (an "original" and a "modified" version) and automatically generates the command file needed to transform one into the other. This is a classic "file difference" analysis.

-   **Input:** Two log files representing a "before" and "after" state.
-   **Output:** A command file containing the exact `REPLACE`, `INSERT`, and `DELETE` instructions required to replicate the changes.

</details>

---
## Technologies Used
- **Python 3**
- Standard libraries: `os`, `sys`, `re`, `collections`
