'''
Python RSA Encryptor/Decryptor/Keygen
for ISEC Course

by: 766102

Known bugs: crashes when trying to decrypt something that is
	not encrypted using this program
	
'''

import sys
import rsalib

def usage():
	print ("usage: rsa.py keygen")
	print ("       rsa.py encrypt \"plaintext\"")
	print ("       rsa.py decrypt \"encrypted text\"")


if (len(sys.argv)) < 2:
	usage()
else:
	if sys.argv[1] == "keygen" or sys.argv[1] == "key-gen":
		print("key: N=%d, e=%d, d=%d" % rsalib.keygen())
	elif sys.argv[1] == "encrypt" or sys.argv[1] == "decrypt":
		if len(sys.argv) < 3:
			usage()
		else:
			if sys.argv[1] == "encrypt":
				print(rsalib.encrypt(sys.argv[2]))
			else:
				print(rsalib.decrypt(sys.argv[2]))
	else:
		usage()
