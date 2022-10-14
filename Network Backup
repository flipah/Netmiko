from netmiko import ConnectHandler
from getpass import getpass
from netmiko import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from paramiko.ssh_exception import AuthenticationException

# creates user inputed variables to re-use later
username = input('Enter your SSH username: ')
password = getpass()

with open('devices_file') as a:
    devices_list = a.read().splitlines()

# opens a file contaning the IPs of the network devices
# uses the username/password vairables inputed to login to the device
for devices in devices_list:
    print ('Connecting to device" ' + devices)
    ip_address_of_device = devices
    ios_device = {
        'device_type': 'cisco_ios',
        'ip': ip_address_of_device, 
        'username': username,
        'password': password
    }
    
    # prints out common errors to assist with troubleshooting
    # prevents the script from completely stopping and will continue
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

    # Enter enable mode, issue command, and disconnect
    net_connect.enable()
    results = net_connect.send_command('show run')
    net_connect.disconnect() 

    # Write output to a file
    filename = f"{ip_address_of_device}.txt"
    file = open( 
        f"{filename}", 'w')
        #f"\\192.168.37.19\\home\\J6 Docs\\Network Automation\\Device Backup\\{filename}", 'w') ------- need to figure this out
    file.write(results)
    file.close()
