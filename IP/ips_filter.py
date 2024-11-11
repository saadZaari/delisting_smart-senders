import os
import re

def filter_ips_from_file():
    # Lists to hold filtered IPs
    bl40_ips = []
    bl50_ips = []

    # Determine the path to 'filtre.txt' located in the same directory as the script
    current_folder = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(current_folder, "filtre.txt")

    # Check if 'filtre.txt' exists, and if not, exit the program
    if not os.path.exists(input_file_path):
        print(f"'filtre.txt' not found in {current_folder}. Please create the file and add IPs.")
        input("Press Enter to exit...")
        return

    # Read data from 'filtre.txt' with UTF-8 encoding
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = file.readlines()

    # Loop through each line in the input data
    for line in data:
        # Find IP address and BL label in the line
        match_ip = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)  # Regex to find IP addresses
        match_bl = re.search(r'BL\d{2}', line)  # Regex to find BL40, BL50 labels

        # Debug: Show what was matched
        if match_ip:
            print(f"Found IP: {match_ip.group(0)}")
        else:
            print(f"No IP found in line: {line}")

        if match_bl:
            print(f"Found BL label: {match_bl.group(0)}")
        else:
            print(f"No BL label found in line: {line}")

        if match_ip and match_bl:
            ip_address = match_ip.group(0)
            bl_label = match_bl.group(0)

            # Add IP address to the corresponding list based on the BL label
            if bl_label == 'BL40':
                bl40_ips.append(ip_address)
            elif bl_label == 'BL50':
                bl50_ips.append(ip_address)

    # Save the filtered IPs to output files in the same directory as the script
    bl40_file_path = os.path.join(current_folder, "BL40.txt")
    with open(bl40_file_path, 'w') as outfile_bl40:
        for ip in bl40_ips:
            outfile_bl40.write(f"{ip}\n")

    bl50_file_path = os.path.join(current_folder, "BL50.txt")
    with open(bl50_file_path, 'w') as outfile_bl50:
        for ip in bl50_ips:
            outfile_bl50.write(f"{ip}\n")

    print("Filtering completed successfully. Check 'BL40.txt' and 'BL50.txt'.")

if __name__ == "__main__":
    filter_ips_from_file()
    input("Press Enter to exit...")  # Pause the script to prevent immediate closure

