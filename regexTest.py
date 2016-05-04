import re
import sys

pattern = r"\([^)]+?\)"
prog = re.compile(pattern)
print sys.argv[1]
result = prog.findall(sys.argv[1])
print len(result)