#!/usr/bin/env python3
####################################
import serial
import os 
import time
import sys
import serial.tools.list_ports
import argparse
from pathlib import Path
####################################

parser = argparse.ArgumentParser()
parser.add_argument("-baud", default="115200", help="baudrate (default \"115200\")")
parser.add_argument("-port", default="COM3", help="port name (default \"COM3\")")
parser.add_argument("-bin",default="main.bin", help="location of the bin file (default \"main.bin\")")
args = parser.parse_args()

#access the serial port
ser =  serial.Serial(args.port,args.baud)

#open binary file 
f = open(args.bin,"rb+")

pageno = 0
program_ended = False

skip = False
sentOnce = False

tstart=time.time()

while True:
	if not sentOnce:
		time.sleep(0.1)
		ser.write("#".encode("ASCII"))
	
	if ser.inWaiting() > 0:
		sentOnce = True
		s=ser.read(1)

		# print("*************************")
		# print("Received response for a ")
		# print(s)
		# print("*************************")
       
		if s == b'a':
			# time.sleep(1)
			ser.write(b'\x00')
			ser.write(b'\x00')
			ser.write("a".encode("ASCII"))		

			while True:
				sum=0
				f.seek(pageno*256,0)
				#time.sleep(0.1)
				time.sleep(0.02) # 0.01 second delay sometimes causes "error: bootloader not responding" print in windows
				
				for i in range(256):
					dataByte = f.read(1)
				    #no more data to send send 'FF' byte and also signal end of send
					if not dataByte:
						program_ended = True
						dataByte = b'\xFF'

					ser.write(dataByte)
					# time.sleep(0.001)

					sum = sum + int.from_bytes(dataByte ,"little")
				sum = sum % 256

				start_waiting_time = time.time()
				while not ser.inWaiting() > 0:
					if time.time()-start_waiting_time > 5:
						print("error boot-loader not responding")
						ser.close()
						sys.exit()

				#read checksum
				checkSum = ser.read(1)
				#convert to int
				checkSum = int.from_bytes(checkSum , "little")
				#check if data is error free 
				addWithCheckSum  = (sum + checkSum) % 256

				if addWithCheckSum != 0:
				    ser.write('$'.encode("ASCII"))
				    print("checksum failed")
				elif program_ended:
					ser.write('!'.encode("ASCII"))

					print("program ends")
					print("time taken to flash(seconds) : ",time.time()-tstart)
					# time.sleep(1)
					ser.close()
					sys.exit()
				else:
				    ser.write('a'.encode("ASCII"))
				    print("one page write complete")
				    pageno += 1
ser.close()
f.close()
