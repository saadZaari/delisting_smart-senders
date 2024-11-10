import configparser
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import os

# Automatically detect the script directory and locate geckodriver
script_dir = os.path.dirname(os.path.abspath(__file__))
geckodriver_path = os.path.join(script_dir, 'geckodriver.exe')

# Set up Firefox options
firefox_options = FirefoxOptions()
firefox_options.add_argument("--start-maximized")
firefox_options.headless = False  # You need to see the browser to interact with the extension

# Initialize WebDriver with the path from config
driver = webdriver.Firefox(service=FirefoxService(executable_path=geckodriver_path), options=firefox_options)

def read_ips_from_file():
    """Read IPs from a text file and return a list of IP addresses."""
    filename = 'BL40.txt'
    with open(filename, 'r') as file:
        ips = [line.strip() for line in file if line.strip()]
    return ips

def submit_ip(ip, index, total):
    """Submit a single IP address to the form."""
    try:
        print(f"Submitting IP {index}/{total}: {ip}")

        # Wait for the form elements to be available
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'IssueTitle')))
        
        # Fill out the form
        driver.find_element(By.ID, 'IssueTitle').send_keys("I can't send a message to my customer")
        driver.find_element(By.ID, 'ContactName').send_keys("  ")
        driver.find_element(By.ID, 'DomainTo').send_keys("hotmail.com")

        # Select timezone
        timezone_select = Select(driver.find_element(By.ID, 'ddlTimezones'))
        timezone_select.select_by_visible_text("(UTC-07:00) Yukon")

        driver.find_element(By.ID, 'DomainFrom').send_keys("no-reply@stollebrot.de")

        # Select company description
        company_description_select = Select(driver.find_element(By.ID, 'SelfDescription'))
        company_description_select.select_by_visible_text("Business (non-marketing)")

        driver.find_element(By.ID, 'WebsiteUrl').send_keys("stollebrot.de")

        # Select server type
        server_type_select = Select(driver.find_element(By.ID, 'ServerType'))
        server_type_select.select_by_visible_text("Shared")

        # Fill in IP addresses
        ip_addresses_textarea = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'IpAddresses'))
        )
        ip_addresses_textarea.clear()
        ip_addresses_textarea.send_keys(ip)
        
        # Fill in the error message
        error_message = f'Error: "550 5.7.1 Unfortunately, messages from [{ip}] weren’t sent. Please contact your Internet service provider since part of their network is on our block list (S3140).'
        error_message_textarea = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'ErrorMessages'))
        )
        error_message_textarea.clear()
        error_message_textarea.send_keys(error_message)

        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Click the submit button
        submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        driver.execute_script("arguments[0].scrollIntoView();", submit_button)
        submit_button.click()
        
        # Wait for the confirmation message
        confirmation_message_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.confirmation-message')))
        confirmation_message = confirmation_message_element.text
        if not confirmation_message.strip():
            print(f"Confirmation message is empty for IP {ip}")
        else:
            print(f"Confirmation message received for IP {ip}: {confirmation_message}")

        time.sleep(4)

    except Exception as e:
        return False

    return True

try:
    # Open the VPN extension download link
    driver.get("https://addons.mozilla.org/firefox/downloads/file/4212703/urban_vpn-3.14.0.xpi")
    
    # Wait a few seconds for the extension installation prompt to appear
    time.sleep(5)

    # Navigate to the login page after opening the VPN download link
    driver.get("https://login.microsoftonline.com")
    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Navigate to the form page
    driver.get("https://olcsupport.office.com/")
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, 'IssueTitle')))

    # Read IP addresses from file
    ips = read_ips_from_file()
    total_ips = len(ips)  # Get the total number of IPs

    # Submit each IP address one by one
    for index, ip in enumerate(ips, start=1):  # start=1 for 1-based indexing
        success = submit_ip(ip, index, total_ips)
        if success:
            print(f"IP {index}/{total_ips} ({ip}) submitted successfully.")

        # Refresh the page to reset the form before the next submission
        driver.get("https://olcsupport.office.com/")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'IssueTitle')))

finally:
    driver.quit()
