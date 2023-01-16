#!/usr/bin/env python3
import scapy
import sys
import optparse
import subprocess
import re
import time

def getFlags():
	parser = optparse.OptionParser()
	parser.add_option("-a", "--adapter", dest="adapter", help='specify network adapter to change mac address')
	parser.add_option("-m", "--mac", dest="newMac", help='specify new mac address')
	options, arguements =  parser.parse_args()
	print("[+] Validating input parameters")
	time.sleep(1)
	#validtion
	if not options.adapter:
		print("[-] No network adapter was specified. use the --help for more information")
		sys.exit()
	if not options.newMac:
		print("[-] No mac address was specifies. use the --help option for more information")
		sys.exit()
	return options



#Validating mac addrss
def checkMac(adapter):
	output = subprocess.check_output(["ifconfig", adapter])
	result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", output.decode('utf-8'))
	return(result.group(0))




#changeMAc
def changeMac(adapter, mac):
	print("[+] Attempting to change MAC address")
	time.sleep(1)
	try:
		subprocess.call(["sudo", "ifconfig", adapter, "down"])
		try:
			subprocess.call(["sudo", "ifconfig", adapter, "hw", "ether", mac])
		except:
			print("[-] Could not change mac address of specified apapter at level 2")
			sys.exit()
		finally:
			subprocess.call(["sudo", "ifconfig", adapter, "up"])
	except:
		print("[-] Could not take " + adapter + " down")
		sys.exit()


options = getFlags()
currentMac = checkMac(options.adapter)
print("[+] Current MAC --> "+currentMac)
changeMac(options.adapter, options.newMac)

#Process verification
NewMac = checkMac(options.adapter)
if NewMac != currentMac:
	print("[+] MAC address successfully changed --> "+ NewMac)
else:
	print("[+] Mac address was not changed")


