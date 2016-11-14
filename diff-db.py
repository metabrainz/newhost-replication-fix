#!/usr/bin/env python

import subprocess
from table_info import REPLICATED_TABLES

OLD_DB = "musicbrainz_old_db"
NEW_DB = "musicbrainz_new_db"
OUT_DIR = "out"

for table in sorted(REPLICATED_TABLES.iterkeys()):
    subprocess.call(["./diff-setup.sh", OLD_DB, NEW_DB, table, OUT_DIR])
