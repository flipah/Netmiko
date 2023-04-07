import os
import re
import shutil
from netmiko import ConnectHandler
from getpass import getpass
from netmiko import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from paramiko.ssh_exception import AuthenticationException

# Saves an on-demand username and password as re-usable variables
username = input('Enter your SSH username: ')
password = getpass()

# Opens the device file and takes out any spaces or added lines
with open('device_file') as f:
    device_list = f.read().splitlines()

# Starts the connection for the devices
for devices in device_list:
    print('Connecting to ' + devices)
    ip_address_of_device = devices
    ios_device = {
        'device_type': 'cisco_ios',
        'ip': ip_address_of_device,
        'username': username,
        'password': password
    }

    # This is for error handeling
    try:
        net_connect = ConnectHandler(**ios_device)
    except (AuthenticationException):
        print ('Authentication failure: ' + ip_address_of_device)
        continue
    except (NetMikoTimeoutException):
        print ('Timeout to device: ' + ip_address_of_device)
        continue
    except (EOFError):
        print ('End of file while attempting device ' + ip_address_of_device)
        continue
    except (SSHException):
        print ('SSH Issue. Are you sure SSH is enabled? ' + ip_address_of_device)
        continue
    except Exception as unknown_error:
        print ('Some other error: ' + str(unknown_error))
        continue
    
    # Connects to the device and only goes into enable mode
    net_connect.enable()
    results = net_connect.send_command('show run')
    net_connect.disconnect()

    # Write output to a file
    filename = f"{ip_address_of_device}.txt"
    file = open( 
        f"{filename}", 'w')
    file.write(results)
    file.close()


    # Open the file and read its contents
    with open(filename, "r") as f:
        contents = f.read()

    # Use a regular expression to search for the hostname
    hostname_pattern = r"hostname\s+(\S+)"
    match = re.search(hostname_pattern, contents)

    # If a hostname was found, rename the file to that hostname
    if match:
        hostname = match.group(1)
        os.rename(filename, hostname + ".txt")
    # Define the path to the directory where the file should be moved
    destination_directory = "Device_Backups"
   
# Move the file to the destination directory, replacing the destination file if it already exists
    try:
        shutil.move(os.path.join(os.getcwd(), hostname + ".txt"), os.path.join(os.getcwd(), destination_directory, hostname + ".txt"))
        print(f"File {hostname}.txt was created and moved to {destination_directory}")
    except shutil.Error as e:
        print(f"Error moving file {hostname}.txt to {destination_directory}: {e}")

    print('Backup completed for ' + hostname)
