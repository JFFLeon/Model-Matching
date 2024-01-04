import os
import re


# Function to read the configuration file
def read_cfg(file_path):
    with open(file_path, 'r') as file:
        return file.read()


# Function to write to the VMR file
def write_vmr(file_path, data, mode='a'):
    with open(file_path, mode) as file:
        file.write(data)  # Write the data to the file


# Function to process the data from the configuration file
def process_data(data):
    icao_type_designator = re.findall(r'icao_type_designator = "(.*?)"', data, re.DOTALL)
    icao_airline = re.findall(r'icao_airline = "(.*?)"', data, re.DOTALL)
    title = re.findall(r'title = "(.*?)"', data, re.DOTALL)

    # Determine the minimum length to avoid index errors
    min_length = min(len(icao_type_designator), len(icao_airline), len(title))

    xml_data = ''
    # Loop through the data and format it as XML
    for i in range(min_length):
        if icao_airline[i]:
            xml_data += '\t<ModelMatchRule CallsignPrefix="{}" TypeCode="{}" ModelName="{}" />\n'.format(
                icao_airline[i], icao_type_designator[i], title[i])
        else:
            xml_data += '\t<ModelMatchRule TypeCode="{}" ModelName="{}" />\n'.format(icao_type_designator[i], title[i])
    return xml_data


# Function to search for the configuration file and write to the VMR file
def search_cfg_and_write_vmr(directory):
    # Use os.walk to iterate through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # If the file is the configuration file
            if file == 'aircraft.cfg':
                print(f'aircraft.cfg found at {os.path.join(root, file)}')  # Debugging output
                cfg_path = os.path.join(root, file)
                # your .vmr file
                vmr_path = 'output.vmr'
                cfg_data = read_cfg(cfg_path)
                vmr_data = process_data(cfg_data)
                print(f'Writing data in {vmr_path}')  # Debugging output
                write_vmr(vmr_path, vmr_data)  # Write the data to the VMR file


# Mod main Folder
# '' < Mod main Folder | Important where there is a "\" must be replaced by 2 "\\"
# My mod Folder Example
dir_path = 'B:\\fsltl-traffic-base'

# Write the XML header to the VMR file
write_vmr('output.vmr', '<?xml version="1.0" encoding="utf-8"?>\n<ModelMatchRuleSet>\n', 'w')
# Call the function to search for the configuration file and write to the VMR file
search_cfg_and_write_vmr(dir_path)
# Write the XML footer to the VMR file
write_vmr('output.vmr', '</ModelMatchRuleSet>')
