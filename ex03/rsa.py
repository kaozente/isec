'''
Python RSA Encryptor/Decryptor/Keygen
'''

import sys
import rsalib

def usage():
	print ("usage: rsa.py keygen")
	print ("       rsa.py encrypt \"plaintext\"")
	print ("       rsa.py decrypt \"encrypted text\"")



rsalib.keygen()


'''
if (len(sys.argv)) < 2:
	usage()
else:
	if sys.argv[1] == "keygen" || sys.argv[1] == "key-gen":
		rsalib.keygen()
	elif sys.argv[1] == "encrypt" || sys.argv[1] == "decrypt":
		if len(sys.argv < 3):
			usage()
		else:
			if sys.argv == "encrypt":
				rsalib.encrypt(sys.argv[2])
			else:
				rsalib.decrypt(sys.argv[2])
	else:
		usage()
'''
