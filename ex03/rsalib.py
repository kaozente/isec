from math import sqrt, ceil
import random 

from dataFileWriter import dataFileWriter

def encrypt(plain):
	pass

def decrypt(crypted):
	pass

def getKey():
	pass

def keygen():

	# Zwei Primzahlen zwischen 100 und 5000
	(p,q) = genPrimes(100,5000,2)
	pv("Two random primes: %d, %d" % (p, q))
	
	n = p*q
	
	phi_n = (p-1)*(q-1)
	pv("Phi(n=p*q): "+str(phi_n))
	
	e = findRandomCoprime(1, phi_n, phi_n)
	pv("e = random number coprime to phi(n): %d (ggt mit %d ist %d)" % (e, phi_n, ggt(e, phi_n)))

	# d * e === 1 mod phi_n
	# e*d + k*phi_n == 1 == ggt(e, phi_n)
	# extended euclid!
	(_, d, _) = xEuclid(e, phi_n)

	# find positive representation
	if d < 0:
		d += phi_n

	pv("found d: %d" % (d))

	# save to file


def saveRsaData(p, q, N, d):
	public = "%d;%d" % (d,N)
	private =  "%d;%d" % (e,N)

	# open file, overwrite existing file
	f = open('crypto.conf', 'w')
	f.write("%d\n%d\n%s\n%s\n" % p, q, public, private)


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
	print(msg)