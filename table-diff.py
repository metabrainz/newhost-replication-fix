#!/usr/bin/env python

import sys
import re
from table_info import REPLICATED_TABLES

p_minus = re.compile('-[0-9]+')
p_plus = re.compile('\+[0-9]+')

if len(sys.argv) < 2:
    print "Usage: %s <table> <diff file>" % sys.argv[0]
    sys.exit(-1)

table = sys.argv[1]
diff = sys.argv[2]

f = open(diff, "r")
if not f:
    print "cannot open diff file"
    sys.exit(-1)

copy_lines = []

print "BEGIN;"
while True:
    line = f.readline()
    if not line:
        break

    line = line.strip()

    if not line:
        continue

    if p_minus.match(line):
        columns = line.split('\t')
        columns[0] = columns[0][1:]
        id = int(columns[0])
        print "DELETE FROM %s WHERE id = %d;" % (table, id)
        continue

    if p_plus.match(line):
        copy_lines.append(line)

f.close()
print "COMMIT;"
print "\COPY %s from stdin" % table
for line in copy_lines:
    print line[1:]
