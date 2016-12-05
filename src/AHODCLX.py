# Import pycomm which is python application for reading / writing to Rockwell Controllers
# Import urllib to POST to Web Service Application
# Import time to timestamp transactions
# Imoprt os, sys for file and directory operations

from pycomm.ab_comm.clx import Driver as ClxDriver
import logging
import urllib
import datetime
from time import sleep
import os, sys


# Define Variables and their defaults. If no AHODCLX.conf exists, these are the values the program will execute with

InAlarm = 0
weburl = "http://imapex-ahod-ahod-server.green.browndogtech.com/ahod"
switchname = 'MFG_IE4K_8GT8GP4GE_1'
switchip = "192.168.90.3"
plcip = '192.168.1.5'
plclocation = 'garagelab'
plcname = 'demo1'
tag1 = 'MachineStop'
cwd = ''
mylog = ''

# Function to check for AHODCLX.conf, read it in and assign to appropriate variables.
# Also establishes AHODLOG.txt for storing output / errors

def var_init():
	global weburl, switchname, switchip, plcip, plclocation, plcname, cwd, mylog, tag1
	cwd = os.path.abspath(os.path.dirname(sys.argv[0]))
	mylog = open(cwd + '/AHODLOG.txt', 'w')
	if os.path.isfile(cwd + "/AHODCLX.conf"):
		print "file found"
		conffile = open(cwd + "/AHODCLX.conf", 'r')
		for line in conffile:
			firstword = line.split(' ')[0]
			lastword = line.split(' ')[2]

			if firstword == 'weburl':
				weburl = lastword
			elif firstword == 'switchname':
				switchname = lastword
			elif firstword == 'switchip':
				switchip = lastword
			elif firstword == 'plcip':
				plcip = lastword
			elif firstword == 'plclocation':
				plclocation = lastword
			elif firstword == 'plcname':
				plcname = lastword
			elif firstword == 'tag1':
				tag1 = lastword
			else:
				print "invalid argument given - " + firstword
				mylog.write("invalid argument given " + firstword + '\n')
		conffile.close()
		print "weburl = " + weburl
		print "switchname = " + switchname
		print "switchip = " + switchip
		print "plcip = " + plcip
		print "plclocation = " + plclocation
		print "plcname = " + plcname
		print "tag1 = " + tag1
		mylog.write("weburl = " + weburl + '\n')
		mylog.write("switchname = " + switchname + '\n')
		mylog.write("switchip = " + switchip + '\n')
		mylog.write("plcip = " + plcip + '\n')
		mylog.write("plclocation = " + plclocation + '\n')
		mylog.write("plcname = " + plcname + '\n')
		mylog.write("tag1 = " + tag1 + '\n')
		mylog.flush()


	else:
		mylog.write('\n' + "No Configuration File Found, using defaults" + '\n')


# Function to send alerts to Web Service Application
# Will attempt to send, if fails ( unable to find in DNS or connectivity down ) it will write to log and continue.

def SendAlert(tagname, value):
    print "ALARM - SENDING AHOD MESSAGE"
    mylog.write("ALARM - SENDING AHOD MESSAGE at " + str(datetime.datetime.now()) + '\n')
    message1 = ''.join(
        ["ALL HANDS ON DECK!, PLC TAG ", tagname, " has a value of ", str(value), " at ", str(datetime.datetime.now())])
    payload = ''.join(["{\n  \"message\": \"", message1, "\",\n  \"plcInfo\": {\n    \"plcDataPoint\": \"", tagname,
                       "\",\n    \"plcIp\": \"", plcip, "\",\n    \"plcLocation\": \"", plclocation,
                       "\",\n    \"plcName\": \"", plcname, "\"\n  },\n  \"switchName\": \"", switchname,
                       "\",\n  \"version\": \"1.0 \"\n}"])
    headers = {'cache-control': "no-cache"}
    try:
    	response = urllib.urlopen(weburl, payload)
    	mylog.write(response.read() + '\n')
    	print(response.read())
    except Exception as e:
	mylog.write("Failed to contact Web App" + '/n')
	mylog.write(e + '/n')
	mylog.flush()

# Main function

if __name__ == '__main__':
	runloop = 1
	var_init()
	('Session information from ' + str(datetime.datetime.now()) + '\n')
	c = ClxDriver()
	mylog.write(str(c['port']) + '\n')
	print c['port']
	mylog.write(str(c.__version__) + '\n')
	print c.__version__
	mylog.flush()
    # attempt to open connection to PLC
	if c.open(plcip):
		while runloop == 1:
			try:
                        # Read value of tag. Only using a single tag currently, future enhancements to enable multiple
                		myMachineStop = str(c.read_tag(tag1))

                        # Data is returned as comma seperated and in paranthesis. Removing formatting to isolate just values
                		myMachineStop = myMachineStop.replace("(", "")
                		myMachineStop = myMachineStop.replace(")", "")
                		myMachineStop = myMachineStop.split(', ')

               			# if the tag was already in alarm, then don't want to send continuous alarms ( For this demo )
                        # Check if already in alarm, if not, put into alarm and call on SendAlert to send to Web Application
                		if int(myMachineStop[0]) == 0 and InAlarm == 1:
                    			InAlarm = 0
                    			mylog.write("Current Value is " + str(myMachineStop[0]) + " and the data type is " + str(myMachineStop[1]) + '\n')
                		elif int(myMachineStop[0]) == 0:
                			InAlarm = 0
                		elif int(myMachineStop[0]) == 1 and InAlarm == 0:
                    			InAlarm = 1
                    			mylog.write("Current Value is " + str(myMachineStop[0]) + " and the data type is " + str(myMachineStop[1]) + '\n')
                    			SendAlert(tag1, myMachineStop[0])
                        # Continues to loop as long as program is running. Current value is to sleep for 1 second. May need to adjust based on PLC load
                		sleep(1)
			except Exception as e:
                		c.close()
                		print e
                		runloop = 0
                		pass


    	c.close()
