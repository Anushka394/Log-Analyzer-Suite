import os
import sys
import re
from collections import defaultdict

# --- 1. Define File Paths ---
# This setup assumes you run the script from the main 'Log-Analyzer-Suite' folder.
base_directory = "Milestone2"
log_path = os.path.join(base_directory, "M2_LogFile.txt")
command_path = os.path.join(base_directory, "M2_CommandFile.txt")
processed_path = os.path.join(base_directory, "M2_ProcessedLogFile.txt")
output_path = os.path.join(base_directory, "M2_Output.txt")

# --- 2. Read Input Files ---
def read_file_lines(file_path):
    """Safely reads all lines from a file and handles FileNotFoundError."""
    try:
        with open(file_path, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"Error: The file was not found at path: {file_path}")
        print("Please ensure the file exists and you are running the script from the correct directory.")
        sys.exit(1) # Exit the script if a required file is missing.

# Read the necessary files.
log_lines = read_file_lines(log_path)
command_lines = read_file_lines(command_path)

print(f"Reading {len(log_lines)} lines from the log file.")
print(f"Found {len(command_lines)} commands to process.")

# --- 3. Process DELETE and INSERT Commands ---
def apply_edits(log_data, command_data):
    """
    Applies 'DELETE' and 'INSERT' commands to the log data.
    """
    lines_to_delete = set()
    lines_to_insert = []
    
    # First, parse all commands to know what to delete and insert.
    for command in command_data:
        command = command.strip()
        if command.startswith("DELETE"):
            try:
                line_index = int(command.split()[1]) - 1 # Convert to 0-based index
                lines_to_delete.add(line_index)
            except (ValueError, IndexError):
                print(f"Warning: Could not parse DELETE command, skipping: {command}")
                
        elif command.startswith("INSERT"):
            # Extract the content that follows the "INSERT " keyword.
            insert_content = command[len("INSERT "):]
            lines_to_insert.append(insert_content + "\n")

    # Build the new list of lines by excluding the ones marked for deletion.
    new_log_data = []
    for i, line in enumerate(log_data):
        if i not in lines_to_delete:
            new_log_data.append(line)
    
    # Add all the new lines to the end of the log.
    new_log_data.extend(lines_to_insert)
    
    print(f"\nProcessing complete. Removed {len(lines_to_delete)} lines and added {len(lines_to_insert)} lines.")
    return new_log_data

# --- 4. Analyze User Logins ---
def count_user_logins(lines):
    """
    Counts how many times each unique user has logged in.
    """
    # defaultdict is useful here as it handles new users automatically.
    login_counts = defaultdict(int)
    
    for line in lines:
        # Use a regular expression to find lines matching the login pattern.
        # This is more robust than splitting the string.
        match = re.search(r"User '(\w+)' logged in", line)
        if match:
            # The username is in the first captured group of the match.
            username = match.group(1)
            login_counts[username] += 1
            
    return login_counts

# --- 5. Execute and Save ---
# Apply the editing commands to the log data.
processed_log_data = apply_edits(log_lines, command_lines)

# Save the newly modified log data to a processed file.
with open(processed_path, "w") as f:
    f.writelines(processed_log_data)

# Count the user logins in the new data.
final_login_counts = count_user_logins(processed_log_data)

# Write the final summary to the output file.
with open(output_path, "w") as f:
    f.write("User Login Counts:\n")
    # Sort the users alphabetically for a clean and predictable report.
    for user, count in sorted(final_login_counts.items()):
        f.write(f"{user}: {count}\n")

# Display a summary of the results to the user.
print("\nFinal User Login Analysis:")
if not final_login_counts:
    print(" - No user login events were found in the processed log.")
else:
    for user, count in sorted(final_login_counts.items()):
        print(f" - User '{user}' logged in {count} time(s).")

print(f"\nScript finished. Output files have been generated in the '{base_directory}' folder.")