import os
import sys

# --- 1. Define File Paths ---
# This setup assumes you run the script from the main 'Log-Analyzer-Suite' folder.
base_directory = "Milestone3"
file1_path = os.path.join(base_directory, "M3_LogFile1.txt")
file2_path = os.path.join(base_directory, "M3_LogFile2.txt")
output_path = os.path.join(base_directory, "M3_Output.txt")

# --- 2. Read Input Files ---
def read_file_lines(file_path):
    """Safely reads all lines from a file and handles FileNotFoundError."""
    try:
        # We strip leading/trailing whitespace from each line as we read it.
        with open(file_path, "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"Error: The file was not found at path: {file_path}")
        print("Please ensure the file exists and you are running the script from the correct directory.")
        sys.exit(1) # Exit the script if a required file is missing.

# Read the two log files that will be compared.
original_lines = read_file_lines(file1_path)
modified_lines = read_file_lines(file2_path)

print(f"Comparing '{os.path.basename(file1_path)}' ({len(original_lines)} lines) with '{os.path.basename(file2_path)}' ({len(modified_lines)} lines).")

# --- 3. Compare Files and Generate Commands ---
def generate_diff_commands(lines1, lines2):
    """
    Compares two lists of strings and generates a list of commands
    (REPLACE, INSERT, DELETE) to transform the first list into the second.
    """
    commands = []
    len1, len2 = len(lines1), len(lines2)
    max_len = max(len1, len2)

    # Iterate through the lists up to the length of the longer list.
    for i in range(max_len):
        line_num = i + 1 # Use 1-based indexing for commands.

        # Case 1: Lines exist in both files.
        if i < len1 and i < len2:
            # If the lines are different, generate a REPLACE command.
            if lines1[i] != lines2[i]:
                commands.append(f'REPLACE {line_num} "{lines2[i]}"')
        
        # Case 2: The line only exists in the second (longer) file.
        elif i < len2:
            commands.append(f'INSERT "{lines2[i]}"')
            
        # Case 3: The line only exists in the first (longer) file.
        elif i < len1:
            commands.append(f'DELETE {line_num}')
            
    return commands

# --- 4. Execute and Save ---
# Generate the list of commands by comparing the two files.
generated_commands = generate_diff_commands(original_lines, modified_lines)

# Write the generated commands to the final output file.
with open(output_path, "w") as f:
    # Join all commands with a newline character for clean formatting.
    f.write("\n".join(generated_commands))

print(f"\nAnalysis complete. Found {len(generated_commands)} differences.")
print(f"A command file has been generated in the '{base_directory}' folder.")