import os
import glob
import time
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
# Locate sensor output file
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Opens the sensors output file and reads in the line for parsing, is stored as a list where the
# the second index contains the temperature data	 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    temp_data = lines[1]
    # lines[1] contains a string with a unique identifier for the sensor, followed by t=xxxx, where xxxx = some temperature
    # I split this string at the = and the second element is the temperature with no decimal place. By taking the first 2 digits I get
    # the celsius value as a whole number. 

    # **** This approach limits the sensor to only read valid values up to 99 ****
    temperature = temp_data.split('=')[1][:2]	
    return temperature
	
while True:
	print(read_temp())	
	time.sleep(1)
