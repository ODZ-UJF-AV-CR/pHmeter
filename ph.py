#!/usr/bin/python
import time
import sys
from pymlab import config

from pylab import *
import time
import numpy as np

import pylirc

color = ['\33[0m','\33[91m','\33[92m','\33[93m','\33[94m','\33[95m','\33[96m']

a = [0, -18.18, -18.18, -18.18, -18.18, -18.18, -18.18]
b = [0, 7.46, 7.46, 7.46, 7.46, 7.46, 7.46]

#### Sensor Configuration ###########################################
cfg = config.Config(
    i2c =
	{
        "port": 1, # I2C bus number
    },

    bus = 
	[
    	{
            "type": "i2chub",
            "address": 0x73, #0x72
            
            "children": 
			[
                {"name": "adc1", "type": "i2cadc01" , "channel": 1, },   
                {"name": "adc2", "type": "i2cadc01" , "channel": 2, },   
                {"name": "adc3", "type": "i2cadc01" , "channel": 3, },   
                {"name": "adc4", "type": "i2cadc01" , "channel": 4, },   
                {"name": "adc5", "type": "i2cadc01" , "channel": 5, },   
                {"name": "adc6", "type": "i2cadc01" , "channel": 6, },   
			],
		},
	],
)

cfg.initialize()
adc = [0,cfg.get_device("adc1"),cfg.get_device("adc2"),cfg.get_device("adc3"),cfg.get_device("adc4"),cfg.get_device("adc5"),cfg.get_device("adc6")]

pylirc.init("pylirc", "/home/odroid/git/pHmeter/conf")

for n in range(9,-1,-1):
	print n,'****** pHmeter www.mlab.cz ******'
	time.sleep(1)
print

try:
    while True:
		newlog = 0
		filename = '/mnt/hroch/chemie/pH/'+str(datetime.datetime.now())+'.log'
		while True:
				s = ''

				for n in range(1,7):
					adc[n].route()
			
					key = pylirc.nextcode()
					if key == ['x']:	
						print color[0]				
						print "*****************************************************"
						print "*************** New Log *****************************"
						newlog = 1
						break


					if n==1:
						# Temperature readout
						temperature = adc[n].readTemp()
						temperature += 7
						print "T","{:+5.1f}".format(temperature),
						print " pH",
					# Voltage readout
					voltage = adc[n].readADC()
					ph = voltage * a[n] + b[n]   #pH
					print color[n], "{:5.2f}".format(ph),
					s += ",{:5.2f}".format(ph)
					#time.sleep(1)
				print color[0]
		
				if newlog == 1:
					break

				with open(filename, 'a') as f:
					f.write("%d,%s" % (time.time(),datetime.datetime.now()))
					f.write("%s\r" % s)
					f.close()


except KeyboardInterrupt:
	f.close()
	sys.exit(0)

