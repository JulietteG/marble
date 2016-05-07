import sys

def progress(n,mod=100):
    if n % mod == 0:
        sys.stderr.write('.')