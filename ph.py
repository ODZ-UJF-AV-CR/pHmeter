#!/usr/bin/python
"""
Testbed for the animation.

It basically produces series of temperatures that get animated on the client
browser side.

"""

import time
import sys
from pymlab import config

import matplotlib
matplotlib.use('module://mplh5canvas.backend_h5canvas')
from pylab import *
import time
import numpy as np

t = [1 + i for i in range(0, 70)]
s = [0]*70
s2 = [0]*70
s[69] = 40
s2[69] = 14

plot(t, s2, linewidth=3.0)
xlabel('time')
ylabel('pH')
title('pH')
f = gcf()
ax = f.gca()

f2 = figure()
ax2 = f2.gca()
ax2.set_xlabel('time')
ax2.set_ylabel('temperature (C)')
ax2.set_title('Temperature internal')
ax2.plot(t, s, linewidth=3.0)

show(block=False, layout=2, open_plot=True)
# show the figure manager but don't block script execution so animation works..

while True:
    #### Sensor Configuration ###########################################
    cfg = config.Config(
        i2c = {
            "port": 1, # I2C bus number
        },

	    bus = [
                {
                "type": "i2chub",
                "address": 0x70,
                
                "children": [
                    {"name": "adc", "type": "i2cadc01" , "channel": 1, },   
			],
                },
            ],
    )



    cfg.initialize()
    adc = cfg.get_device("adc")

    time.sleep(0.5)

    n =  t[-1] + 1
    try:
        while True:
	    adc.route();
            # Temperature readout
            temperature = 0
            temperature = adc.readTemp()
            #temperature -= 1.5
            print "Internal Temperature =", float("{0:.2f}".format(temperature))
           
            time.sleep(1)

            # Voltage readout
            voltage = adc.readADC()
            ph = -(voltage / 0.050) + 7   #pH
            print "Voltage =", voltage, ",  pH =", float("{0:.2f}".format(ph))

            # refresh graph
            s = s[1:] + [ph]
            s2 = s2[1:] + [temperature]
            t = t[1:] + [n]
            n += 1
            if (n % 10) == 0:
                ax.text(n, ph-1, "{0:.2f}".format(ph),
                verticalalignment='bottom', horizontalalignment='right',
                color='red', fontsize=16)
                ax2.text(n, temperature-5, "{0:.1f}".format(temperature),
                verticalalignment='bottom', horizontalalignment='right',
                color='green', fontsize=16)

            ax.lines[0].set_xdata(t)
            ax.lines[0].set_ydata(s)
            ax.set_xlim(t[0],t[-1])
            ax2.lines[0].set_xdata(t)
            ax2.lines[0].set_ydata(s2)
            ax2.set_xlim(t[0],t[-1])
            f.canvas.draw()
            f2.canvas.draw()
            #time.sleep(0.5)




    except IOError:
        print "IOError"
        continue

    except KeyboardInterrupt:
    	sys.exit(0)


