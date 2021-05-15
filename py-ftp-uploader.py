host = ""
username = ""
password = ""
upload_dir = "./build"
port = 21

import os.path, os
from ftplib import FTP, error_perm
import sys,getopt

try:
	opts, args = getopt.getopt(sys.argv[1:],"hhounpwdi:po:",["host=","username=","password=","dir=","port="])
except getopt.GetoptError:
	print ('ftp-upload.py -ho|--host <host:required!> -un|--username <username:required!> -pw|--password <password:required!> -di|--dir <local_directory:./build> -po|--port <port:./21>')
	sys.exit(2)
for opt, arg in opts:
	if opt == '-h':
		print ('ftp-upload.py -ho|--host <host:required!> -un|--username <username:required!> -pw|--password <password:required!> -di|--dir <local_directory:./build> -po|--port <port:./21>')
		sys.exit()
	elif opt in ("-ho", "--host"):
		host = arg
	elif opt in ("-un", "--username"):
		username = arg
	elif opt in ("-pw", "--password"):
		password = arg
	elif opt in ("-di", "--dir"):
		upload_dir = arg
	elif opt in ("-po", "--port"):
		port = arg

ftp = FTP()
ftp.connect(host,port)
ftp.login(username,password)

def placeFiles(ftp, path):
	for name in os.listdir(path):
		localpath = os.path.join(path, name)
		if os.path.isfile(localpath):
			print("STOR "+ name+" @ "+ localpath)
			ftp.storbinary('STOR ' + name, open(localpath,'rb'))
		elif os.path.isdir(localpath):
			print("MKD "+ name)
			try:
				ftp.mkd(name)
			except error_perm as e:
				if not e.args[0].startswith('550'): 
					raise
			print("CWD "+ name)
			ftp.cwd(name)
			placeFiles(ftp, localpath)           
			print("CWD ..")
			ftp.cwd("..")
placeFiles(ftp, upload_dir)
ftp.quit()
print('the directory '+upload_dir+' upload process is complete!')