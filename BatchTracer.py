#This script is easy to use
#Simply drop into a folder with a txt file containing your CIDR-notated subnets and execute the script using:
#python BatchTracer.py
#and then enter the name of the text file containing the desired subnets.
#Your results will be collated into a file named BATCH-RESULTS.txt
#The individual tracert executions will be captured in their own files for closer scrutiny

import os
import re
import calendar
import time
import sys
import fileinput

def check_if_string_in_file(file_name, string_to_search, second_string_to_search, third_string_to_search):
	with open(file_name, 'r') as read_obj:
		for line in read_obj:
			if string_to_search in line:
				return remove((re.search("rpan\S*", line)).group())
			if third_string_to_search in line:
				return remove((re.search("rsrx\S*", line)).group())
			if second_string_to_search in line:
				return 'Placeholder for Inline Firewalls'
		return 'Not Behind Firewall'

def remove(string):
	string.strip()
	string.replace("^","")
	string.replace(" ","")
	return string

def iterate(string):
 
    start = string[0]
     
    # storing the last character
    end = int(string[-1])
    cap = str(end + 1)
    iterated_string = string[0:-1] + cap
    ips.append(iterated_string)

    
    return iterated_string

ips = [

]

subnets = [

]

print("Welcome to BatchTracer")
print("Input your subnet list filename (followed by .txt):")
input1 = input()

file1 = open(input1, 'r')
Lines = file1.readlines()

for line in Lines:
    line = remove(line)
    subnets.append(line)


for subnet in subnets:
    x = subnet.split("/")
    y = x[0]
    if (int(x[1]) == 32):
        ips.append(y)
#        print(y)
    else:
        iterated = iterate(y)
#        print(iterated)

x=0

from datetime import datetime

current_GMT = time.gmtime()
ts = calendar.timegm(current_GMT)
dt = datetime.fromtimestamp(ts)

file_object = open ('BATCH-RESULTS.txt', 'a')
file_object.write('\n')
file_object.write('\n')
file_object.write('BatchTracer Tracert Results ' + str(dt))
file_object.write('\n')
file_object.write('\n')
file_object.close()

for ip in ips:
	print('Tracing route to ' + ip)
	os.system('tracert -h 15 ' + ip + ' > tracert-res-' + ip + '.txt')
	with open('Tracert-res-staging.txt', 'a+') as file_object:
		file_object.write(subnets[x])
		file_object.close()
	string = check_if_string_in_file('tracert-res-' + ip + '.txt', 'rpan', 'rmpf', 'rsrx')			
	input_file = fileinput.input('Tracert-res-staging.txt', inplace=1)
	for line in input_file:
		if line.startswith(subnets[x]):
			string =  line.strip() + ' ' + string
		else:
			print ('q' + line)
	input_file.close()
	file_object = open ('BATCH-RESULTS.txt', 'a')
	file_object.write('\n')
	file_object.write(string)
	file_object.close()
	x = x + 1
	print('Trace complete')

from datetime import datetime

current_GMT = time.gmtime()
ts = calendar.timegm(current_GMT)
dt = datetime.fromtimestamp(ts)

file_object = open ('BATCH-RESULTS.txt', 'a')
file_object.write('\n')
file_object.write('\n')
file_object.write('Run concluded: ' + str(dt))
file_object.write('\n')
file_object.write('\n')
file_object.close()

print('Batch Complete')
os.remove('Tracert-res-staging.txt')
sys.exit()
