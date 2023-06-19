#!/usr/bin/env python3
##################################
import argparse
from pathlib import Path
import os
##################################



if __name__ == "__main__":

	parser = argparse.ArgumentParser()

	parser.add_argument("-baud", default="115200", help="baudrate (default \"115200\")")
	parser.add_argument("-bin",default="main.bin", help="location of the bin file (default \"main.bin\")")
	parser.add_argument("-cpu",default="atmega2560", help="atmega2560 or esp32 (default \"atmega2560\")")
	parser.add_argument("-exe",default="\\hardware\\tools\\avr\\bin", help="location of the flasher exe in Arduino-IDE (default \"\\hardware\\tools\\avr\\bin\")")
	parser.add_argument("-ip",default="192.168.4.1", help="IP address for wireless flashing (default \"192.168.4.1\")")
	parser.add_argument("-mode",default="wired", help="wired, wireless-u, wireless-uf (default \"wired\")")
	parser.add_argument("-port",default="/dev/ttyUSB0", help="port name (default \"/dev/ttyUSB0\")")

	args = parser.parse_args()

	#-----------------------------

	if args.cpu == "atmega2560":
		if args.mode == "wired":
			flash_cmd = f"{args.exe}/eyfi-mega-avr-flasher -baud={args.baud} -port={args.port} -bin={args.bin}"
			print()
			os.system(flash_cmd)
		elif args.mode == "wireless-u":
			pass
		elif args.mode == "wireless-uf":
			pass

		

