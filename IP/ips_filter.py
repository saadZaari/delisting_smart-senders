import os
import re

def filter_ips_from_input():
    # Lists to hold filtered IPs
    bl40_ips = []
    bl50_ips = []

    print("Paste the data below (press Enter twice when done):")

    # Reading the pasted data until an empty line is entered
    data = []
    while True:
        line = input()  # Read line from the user input
        if not line.strip():  # If the line is empty, stop reading
            break
        data.append(line)

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

    # Determine the base folder where BL40.txt and BL50.txt should be saved
    # For example, assume they are stored in an 'ips' folder within the current script’s directory.
    current_folder = os.path.dirname(os.path.abspath(__file__))
    ips_folder = os.path.join(current_folder)  # Adjust this if the folder is different

    # Ensure the 'ips' directory exists
    os.makedirs(ips_folder, exist_ok=True)

    # Write the filtered BL40 IPs to the output file in the 'ips' folder
    bl40_file_path = os.path.join(ips_folder, "BL40.txt")
    with open(bl40_file_path, 'w') as outfile_bl40:
        for ip in bl40_ips:
            outfile_bl40.write(f"{ip}\n")

    # Write the filtered BL50 IPs to the output file in the 'ips' folder
    bl50_file_path = os.path.join(ips_folder, "BL50.txt")
    with open(bl50_file_path, 'w') as outfile_bl50:
        for ip in bl50_ips:
            outfile_bl50.write(f"{ip}\n")

    print("Filtering completed successfully. Check 'ips/BL40.txt' and 'ips/BL50.txt'.")

if __name__ == "__main__":
    filter_ips_from_input()
