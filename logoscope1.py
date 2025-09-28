import os
import sys
# --- 1. Define File Paths ---
# This setup assumes you run the script from the main 'Log-Analyzer-Suite' folder.
# It correctly points to the files inside the 'Milestone1' subfolder.
base_directory = "Milestone1"
log_path = os.path.join(base_directory, "M1_LogFile.txt")
command_path = os.path.join(base_directory, "M1_CommandFile.txt")
processed_path = os.path.join(base_directory, "M1_ProcessedLogFile.txt")
output_path = os.path.join(base_directory, "M1_Output.txt")

# --- 2. Read Input Files ---
# A function to safely read files and handle errors if they are not found.
def read_file_lines(file_path):
    """Safely reads all lines from a file and handles FileNotFoundError."""
    try:
        with open(file_path, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"Error: The file was not found at path: {file_path}")
        print("Please ensure the file exists and you are running the script from the correct directory.")
        sys.exit(1) # Exit the script if a required file is missing.

# Read the necessary files using the safe function.
log_lines = read_file_lines(log_path)
command_lines = read_file_lines(command_path)

print(f"Reading {len(log_lines)} lines from the log file.")
print(f"Found {len(command_lines)} REPLACE commands to process.")

# --- 3. Process REPLACE Commands ---
def apply_replacements(log_data, command_data):
    """
    Goes through each command and applies the 'REPLACE' action to the log data.
    """
    lines_replaced = 0
    lines_skipped = 0
    
    for command in command_data:
        if command.strip().startswith("REPLACE"):
            parts = command.split(" ", 2)
            
            # Skip any command that isn't formatted correctly.
            if len(parts) < 3:
                continue
            
            try:
                # Convert the line number from the command to a list index (by subtracting 1).
                line_index = int(parts[1]) - 1
                new_content = parts[2].strip()

                # Check if the line number is valid for the log file.
                if 0 <= line_index < len(log_data):
                    # Keep the original timestamp but replace the rest of the line.
                    timestamp = log_data[line_index].split("]", 1)[0] + "]"
                    log_data[line_index] = f"{timestamp} {new_content}\n"
                    lines_replaced += 1
                else:
                    # If the line number doesn't exist, skip it and notify the user.
                    print(f"Warning: Skipped command for line {line_index + 1} as it is out of range.")
                    lines_skipped += 1
            except ValueError:
                print(f"Warning: Could not parse command, skipping: {command.strip()}")
                lines_skipped += 1
                
    print(f"\nProcessing complete. Total lines replaced: {lines_replaced}")
    if lines_skipped > 0:
        print(f"Total commands skipped due to errors: {lines_skipped}")
        
    return log_data

# --- 4. Analyze Log Data ---
def count_log_levels(lines):
    """
    Counts the total number of INFO, ERROR, and WARN messages in the log data.
    """
    counts = {"INFO": 0, "ERROR": 0, "WARN": 0}
    for line in lines:
        if "] INFO" in line:
            counts["INFO"] += 1
        elif "] ERROR" in line:
            counts["ERROR"] += 1
        elif "] WARN" in line:
            counts["WARN"] += 1
    return counts

# --- 5. Execute and Save ---
# Apply the replacement commands to the log data.
processed_log_data = apply_replacements(log_lines, command_lines)

# Save the newly modified log data to a processed file.
with open(processed_path, "w") as f:
    f.writelines(processed_log_data)

# Count the log levels in the new data.
final_counts = count_log_levels(processed_log_data)

# Write the final summary to the output file.
with open(output_path, "w") as f:
    f.write(f"INFO: {final_counts['INFO']}\n")
    f.write(f"ERROR: {final_counts['ERROR']}\n")
    f.write(f"WARN: {final_counts['WARN']}\n")

# Display the final results to the user.
print("\nFinal Log Analysis Results:")
print(f" - INFO messages: {final_counts['INFO']}")
print(f" - ERROR messages: {final_counts['ERROR']}")
print(f" - WARN messages: {final_counts['WARN']}")
print(f"\nScript finished. Output files have been generated in the '{base_directory}' folder.")