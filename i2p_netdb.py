"""
Author: Michael Straughan
Date: 16/05/2013
Description: scrapes all files in /i2p/netDb for router IPs and remote ports for trivial recon
Usage: i2p_netdb.py <i2p_netdb_path>
"""

import os
import os.path
import sys
import re

def get_files(path):
	filelist = []
	for root, dirs, files in os.walk(path):
		for filename in files:
			filelist.append(os.path.join(root,filename))
	return filelist

if len(sys.argv) < 2:
	if sys.platform == "win32":
		directory = os.environ['APPDATA']+"\\i2p\\netDb"
	elif sys.platform == "linux":
		directory = "~/.i2p/netDb"
	else:
		directory = sys.argv[1]
else:
	directory = sys.argv[1]

files = get_files(directory)
for file in files:
	f = open(file, "rb")
	if f:
		content = f.read()
		if content:
			host = re.search(b"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", content)
			if host:
				print("Host: %s " % host.group(0).decode("utf-8"))
				
			port = re.search(b"(?<=port\=[\x00-\xff])\d{1,5}", content)
			if port:
				print("Port: %s" % port.group(0).decode("utf-8"))
		else:
			print("cant read file")
		f.close()
		print("----")
	else:
		print("cant open file")