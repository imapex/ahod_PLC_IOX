# Import pycomm which is python application for reading / writing to Rockwell Controllers

from pycomm.ab_comm.clx import Driver as ClxDriver
import logging
import urllib
import datetime
from time import sleep
import os

InAlarm = 0

# pull message variables from environment variables if set, else use defaults
if ("weburl" in os.environ):
    weburl = os.getenv("weburl")
else:
    weburl = "http://imapex-ahod-ahod-server.green.browndogtech.com/ahod"
if ("switchname" in os.environ):
    switchname = os.getenv("switchname")
else:
    switchname = 'MFG_IE4K_8GT8GP4GE_1'
if ("switchip" in os.environ):
    switchip = os.getenv("switchip")
else:
    switchip = "192.168.90.3"
if ("plcip" in os.environ):
    plcip = os.getenv("plcip")
else:
    plcip = '192.168.1.5'
if ("plclocation" in os.environ):
    plclocation = os.getenv("plclocation")
else:
    plclocation = 'garagelab'
if ("plcname" in os.environ):
    plcname = os.getenv("plcname")
else:
    plcname = 'demo1'


def SendAlert(tagname, value):
    print "ALARM - SENDING AHOD MESSAGE"
    f.write("ALARM - SENDING AHOD MESSAGE" + '\n')
    message1 = ''.join(
        ["ALL HANDS ON DECK!, PLC TAG ", tagname, " has a value of ", str(value), " at ", str(datetime.datetime.now())])
    payload = ''.join(["{\n  \"message\": \"", message1, "\",\n  \"plcInfo\": {\n    \"plcDataPoint\": \"", tagname,
                       "\",\n    \"plcIp\": \"", plcip, "\",\n    \"plcLocation\": \"", plclocation,
                       "\",\n    \"plcName\": \"", plcname, "\"\n  },\n  \"switchName\": \"", switchname,
                       "\",\n  \"version\": \"1.0 \"\n}"])
    headers = {'cache-control': "no-cache"}
    response = urllib.urlopen(weburl, payload)
    f.write(response.read() + '\n')
    print(response.read())


if __name__ == '__main__':
	runloop = 1
	f = open('AHODLOG.txt', 'w')
	f.write('Session information from ' + str(datetime.datetime.now()) + '\n')
	c = ClxDriver()
	f.write(str(c['port']) + '\n')
	print c['port']
	f.write(str(c.__version__) + '\n')
	print c.__version__
	f.flush()
	if c.open(plcip):
		while runloop == 1:
			try:
				tag1 = 'MachineStop'
                		myMachineStop = str(c.read_tag(tag1))
                		myMachineStop = myMachineStop.replace("(", "")
                		myMachineStop = myMachineStop.replace(")", "")
                		myMachineStop = myMachineStop.split(', ')
               			#print "Current Value is ", myMachineStop[0], " and the data type is ", myMachineStop[1]
                		if int(myMachineStop[0]) == 0 and InAlarm == 1:
                    			InAlarm = 0
                    			f.write("Current Value is " + str(myMachineStop[0]) + " and the data type is " + str(myMachineStop[1]) + '\n')
                		elif int(myMachineStop[0]) == 0:
                			InAlarm = 0
                		elif int(myMachineStop[0]) == 1 and InAlarm == 0:
                    			InAlarm = 1
                    			f.write("Current Value is " + str(myMachineStop[0]) + " and the data type is " + str(myMachineStop[1]) + '\n')
                    			SendAlert(tag1, myMachineStop[0])
                		sleep(1)
			except Exception as e:
                		c.close()
                		print e
                		runloop = 0
                		pass


    	c.close()
