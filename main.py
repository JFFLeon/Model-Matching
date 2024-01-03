import os, re


# Here it reads the cfg
def read_cfg(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data


# Here he writes the vmr
def write_vmr(file_path, data, mode='a'):
    with open(file_path, mode) as file:
        file.write(data)


# this is where the varibable Defination
def process_data(data):
    icao_type_designator = re.findall(r'icao_type_designator = "(.*?)"', data, re.DOTALL)
    icao_airline = re.findall(r'icao_airline = "(.*?)"', data, re.DOTALL)
    title = re.findall(r'title = "(.*?)"', data, re.DOTALL)

    # so that the index error does not occur
    min_length = min(len(icao_type_designator), len(icao_airline), len(title))

    xml_data = ''
    for i in range(min_length):
        if icao_airline[i]:
            xml_data += '\t<ModelMatchRule CallsignPrefix="{}" TypeCode="{}" ModelName="{}" />\n'.format(
                icao_airline[i], icao_type_designator[i], title[i])
        else:
            xml_data += '\t<ModelMatchRule TypeCode="{}" ModelName="{}" />\n'.format(icao_type_designator[i], title[i])
    return xml_data


# Here it searches for the cfg and writes it in the vmr
def search_cfg_and_write_vmr(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'aircraft.cfg':
                print('aircraft.cfg found !')  # Debugging output
                cfg_path = os.path.join(root, file)
                vmr_path = 'output.vmr'
                cfg_data = read_cfg(cfg_path)
                vmr_data = process_data(cfg_data)
                print(f'Write data in {vmr_path}')  # Debugging output
                write_vmr(vmr_path, vmr_data)


# Mod main Folder
# '' < Mod main Folder | Important where there is a "\" must be replaced by 2 "\\"
# My mod Folder Example
dir_path = 'C:\\fsltl-traffic-base'

# writes things to the output.vmr
write_vmr('output.vmr', '<?xml version="1.0" encoding="utf-8"?>\n<ModelMatchRuleSet>\n', 'w')
search_cfg_and_write_vmr(dir_path)
write_vmr('output.vmr', '</ModelMatchRuleSet>')
