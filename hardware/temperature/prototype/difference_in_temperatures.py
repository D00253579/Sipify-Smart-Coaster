import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'

# setup contact sensor
contact_folder = glob.glob(base_dir + '28*')[0]
contact_file = contact_folder + '/w1_slave'

# setup submergible sensor
submergible_folder = glob.glob(base_dir + '28*')[1]
submergible_file = submergible_folder + '/w1_slave'

def write_to_file(contact_temp, submergible_temp):
    with open('temperature_difference_test.txt', 'a') as file:
        file.write(f"Contact: {contact_temp}°C | Submerg: {submergible_temp}°C | Timestamp: {time.strftime('%H:%M:%S')}\n")


def read_temp_raw(file):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(file):
    lines = read_temp_raw(file)
    temp_data = lines[1]
    temperature = temp_data.split('=')[1][:2]	
    return temperature

while True:
    contact_temp = read_temp(contact_file)
    submergible_temp = read_temp(submergible_file)

    print(f"Contact: {contact_temp}")
    print(f"Submerg: {submergible_temp}")

    #write_to_file(contact_temp, submergible_temp)
    time.sleep(0.5) 
