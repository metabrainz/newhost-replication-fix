#!/usr/bin/env python

import subprocess
import sys
from table_info import REPLICATED_TABLES

if len(sys.argv) < 3:
    print "Specify two database names to compare."

OLD_DB = sys.argv[1]
NEW_DB = sys.argv[2]

for table in sorted(REPLICATED_TABLES.iterkeys()):
    subprocess.call(["./diff-table.sh", OLD_DB, NEW_DB, table])
