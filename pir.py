#!/usr/bin/python +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|-|S|p|y|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# pir_1.py Detect movement using a PIR module
#
# Author : Matt Hawkins Date : 21/01/2013 Import required Python libraries
# Editor: Jonas Eichler
# for more performance do not check each ms/tic, use sleep
import RPi.GPIO as GPIO 
import time
import os

# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
# Define GPIO to use on Pi and set pin as input
GPIO_PIR = 4
GPIO.setup(GPIO_PIR,GPIO.IN) # Echo 

print "PIR Module Test (CTRL-C to exit)"
Current_State = 0 
Previous_State = 0 

try:
  print "Waiting for PIR to settle ..."
  # Loop until PIR output is 0
  while GPIO.input(GPIO_PIR)==1:
    Current_State = 0
  print " Ready"
    
  # Loop until users quits with CTRL-C
  while True :
   
    # Read PIR state
    Current_State = GPIO.input(GPIO_PIR)
   
    if Current_State==1 and Previous_State==0:
      # PIR is triggered     
      cnt = 0
      while cnt < 2:
		os.system("pilight-send -p intertechno_switch -i 13244170 -u 1 -t")
		cnt = cnt+1
		time.sleep(0.5)
      time.sleep(28) # keep light on
      
      # enable switch off only if there was no movement for 5 seconds
      start = time.time()
      while time.time() < start + 5:	
	Current_State = GPIO.input(GPIO_PIR)
      	if Current_State == 1:
		start = time.time()
	time.sleep(0.1)
	
      # Record previous state
      Previous_State=1
    elif Current_State==0 and Previous_State==1:
      # PIR has returned to ready state   
      os.system("pilight-send -p intertechno_switch -i 13244170 -u 1 -f")
      time.sleep(0.1) # sleep so that switching on will work again
      Previous_State=0
      
    # Wait for 100 milliseconds
    time.sleep(0.1)
      
except KeyboardInterrupt:
  print " Quit"
  GPIO.cleanup()