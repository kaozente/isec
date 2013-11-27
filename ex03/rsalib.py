from math import sqrt, ceil
import random 
import base64
from struct import pack, unpack

from dataFileWriter import dataFileWriter

def encrypt(plain):
	'''
	encrypt given message m:
	c === m^e mod N
	'''

	pv("Encrypting " + plain)

	# obtain public key
	N, e, _ = getKeys()

	# convert plaintext to encryptable list of shorts
	blocks = stringToShortBlocks(plain)
	pv("plain blocks: " + str(blocks))

	cipher = []

	# encrypt each block
	for block in blocks:
		# ciBlock = block**e % N # works, but is unsurprisingly really slow
		ciBlock = pow(block, e, N)
		cipher.append(ciBlock)
		pv("one block down!")

	pv("cipher blocks: " + str(cipher))

	# convert blocks back to string
	ciString = ciBlocksToString(cipher)

	return ciString


def decrypt(cipher):
	
	pv("Decrypting " + cipher)

	# obtain private key
	N, _, d = getKeys()

	# convert chipherstring to decryptable list of ints
	ciBlocks = stringToCiBlocks(cipher)
	pv(str(ciBlocks))

	# decrypt each block to a plaintext short block
	blocks = []
	for block in ciBlocks:
		#blocks.append(block**d % N)
		blocks.append(pow(block, d, N))
		pv("one block down.")

	pv("freshly decryptet plain blocks: " + str(blocks))

	plain = shortBlocksToString(blocks)
	pv(plain)

	return plain

def keygen():
	return keygenUsing(*genPrimes(100,5000,2))

def keygenUsing(p,q):

	n = p*q
	
	phi_n = (p-1)*(q-1)
	pv("Phi(n=p*q): "+str(phi_n))
	
	e = findRandomCoprime(1, phi_n, phi_n)
	pv("e = random number coprime to phi(n): %d (gcd is %d)" % (e, ggt(e, phi_n)))

	# d * e === 1 mod phi_n
	# e*d + k*phi_n == 1 == ggt(e, phi_n)
	# extended euclid!
	(_, d, _) = xEuclid(e, phi_n)

	# find positive representation
	if d < 0:
		d += phi_n

	pv("found d: %d" % (d))

	# save to file
	saveRsaData(p,q,n,d,e)

	pv("keys generated sucessfully!")

	return(n,e,d)


def getKeys():
	'''
	try to load keys from file, if this doesn't work
	generate new ones. returns both keys.
	'''
	ret = loadRsaData() # will return either -1 or a list
	if type(ret) is int:
		# something went wrong, generate new keys!
		pv("generating new keys...")
		return keygen()
	else:
		(p,q,e,d) = ret
		if e < 0: # only primes given
			pv("generating new keys using given primes")
			return keygenUsing(p,q)
		else:
			pv("successfully loaded keys from file")
			return (p*q,e,d)


def saveRsaData(p, q, N, d, e):
	fname = "crypto.conf"

	#public = "%d;%d" % (e,N)
	public = str(e)
	#private =  "%d;%d" % (d,N)
	private = str(d)

	# open file, overwrite existing file, write linebreak sep'd strings
	with open(fname, 'w') as f:
		f.write("%d\n%d\n%s\n%s" % (p, q, public, private))

	pv("Saved Data to " + fname)

def loadRsaData():
	fname = "crypto.conf"
	try:
		with open(fname, 'r') as f:
			# speichern als liste
			vals = f.readlines()
			pv("loaded file, length=%d" % len(vals))
		if len(vals) < 2:
			raise noValidCryptoConf
		else:
			p = int(vals[0])
			q = int(vals[1])
			N = p*q
			pv("loaded p=%d, q=%d" % (p,q))
			if (len(vals) >= 4):
				e = int(vals[2])
				d = int(vals[3])
			else:
				e = d = -1

		#(e, N) = map(int, vals[2].split(";"))
		#pv("loaded public key: e=%d, N=%d" % (e,N))

		#(d, N) = map(int, vals[3].split(";"))
		#pv("loaded private key: d=%d, N=%d" % (d,N))

		return(p,q,e,d)

	except: # not really meaningful here what went wrong, we'll just generate new keys
		pv("Error loading Keys from File!")
		return -1



def genPrimes(start, end, nr=1):
	primes = []
	for i in range(nr):
		cand = 1
		while isPrime(cand) != 1 or cand in primes:
			cand = random.randrange(start, end)
		primes.append(cand)
	return primes



def isPrime(nr):
	# range does not include last element, thus +1
	if nr < 2:
		return 0
	for i in range(2,ceil(sqrt(nr))+1):
		if nr % i == 0 and nr != i:
			return 0
	return 1

def findRandomCoprime(start, end, co):
	cand = 0
	while 1:
		cand = random.randrange(start, end)
		if ggt(cand, co) == 1:
			return cand

def ggt(x, y):
        return not y and x or ggt(y,x%y)


def stringToShortBlocks(s):
	'''
	convert plain(string) -> bytes -> list of shorts
	'''

	plainbytes = bytearray(s, 'utf-8')

	# pad if necessary (stupid padding, not like in RSA RFC)
	if len(plainbytes) % 2 == 1:
		# append NUL
		plainbytes.append(0x00) 
		pv("padded string")
		
	return unpack(("H"*(len(plainbytes)//2)), plainbytes)

def shortBlocksToString(blocks):
	plain = pack("H"*len(blocks), *blocks).decode('ascii')
	if plain[-1] == "\x00":
		pv("PADDDDDDING!!!!!")
		return plain[:-1]

	return plain


def ciBlocksToString(slist):
	'''
	convert list of ints -> bytes -> bytes(b64) -> ascii string
	'''

	b = pack("I"*len(slist), *slist) # * unpacks list
	return base64.b64encode(b).decode('ascii')


def stringToCiBlocks(s):
	bytes = base64.b64decode(s)
	ilst = unpack("I"*(len(bytes)//4),bytes)
	return ilst



def xEuclid(a,b):

	''' 
	compute linear combination: u*a + v*b == ggt(a,b)
	'''

	u = t = 1
	v = s = 0

	while b > 0:
		q = a // b # // = div
		a, b = b, a - q*b
		u, s = s, u - q*s
		v, t = t, v - q*t

	return a, u, v

def pv(msg):
	''' 
	comment / uncomment to print verbose
	'''
	#print(msg)
	pass