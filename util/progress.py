import sys

def progress(n,mod=100):
	"""
	Display progress with a .
	"""
    if n % mod == 0:
        sys.stderr.write('.')