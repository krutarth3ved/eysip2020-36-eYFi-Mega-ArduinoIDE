#!/usr/bin/env python
import serial
import os 
import time
import sys
import serial.tools.list_ports

comlist = serial.tools.list_ports.comports()
print(comlist)
comport = comlist[0].device
print(comport)
ser =  serial.Serial(comport,115200)

#open binary file 
f = open(sys.argv[1],"rb")


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

		print("*************************")
		print("Received response for a ")
		print(s)
		print("*************************")
       
		if s == b'a':
			

			print("reached")
			# time.sleep(1)
			ser.write(b'\x00')
			# while not (ser.inWaiting() > 0):
			# 	time.sleep(0.001)
			# s = ser.read(1)
			# print(s)

			
			ser.write(b'\x00')
			
			# while not (ser.inWaiting() > 0):
			# 	time.sleep(0.001)
			# s = ser.read(1)
			# print(s)



			ser.write("a".encode("ASCII"))
			# while not (ser.inWaiting() > 0):
			# 	time.sleep(0.001)
			# s = ser.read(1)

	
			# print("++++++++++++++++++++++++")
			# print("Received response  after send ")
			# print(s)
			# print("++++++++++++++++++++++++++")
		
		

			while True:
				sum=0
				f.seek(pageno*256,0)
				# time.sleep(0.1)
				time.sleep(0.01)
				

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
						exit()

	                

	        
				print("waiting end")

				#read checksum
				checkSum = ser.read(1)

				#convert to int
				checkSum = int.from_bytes(checkSum , "little")

				print(checkSum)
				print(sum)

				#check if data is error free 
				addWithCheckSum  = (sum + checkSum) % 256

				print(addWithCheckSum)

				

				if addWithCheckSum != 0:
				    ser.write('$'.encode("ASCII"))
				    print("checksum failed")
				elif program_ended:
					ser.write('!'.encode("ASCII"))

					print("program ends")
					print("time taken to flash(seconds) : ",time.time()-tstart)
					# time.sleep(1)
					exit()
				else:
				    ser.write('a'.encode("ASCII"))
				    print("one page write complete")
				    pageno += 1
