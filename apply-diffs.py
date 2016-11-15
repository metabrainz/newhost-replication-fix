#!/usr/bin/env python

import psycopg2
import codecs
import os
import os.path
import string
import sys
import re
from collections import OrderedDict
from table_info import REPLICATED_TABLES


old_db = psycopg2.connect('dbname=musicbrainz_old_db user=musicbrainz_user host=127.0.0.1 port=5432')


COLUMN_INFO = {}
for table, columns in REPLICATED_TABLES.iteritems():
    for column in columns:
        COLUMN_INFO[table + '.' + column[0]] = column[1:]


## Code adapted from mbslave with some modifications.
## https://bitbucket.org/lalinsky/mbslave/raw/e86f415/mbslave-sync.py

ESCAPES = (('\\b', '\b'), ('\\f', '\f'), ('\\n', '\n'), ('\\r', '\r'),
           ('\\t', '\t'), ('\\v', '\v'), ('\\\\', '\\'))

def unescape(s):
    if s == '\\N':
        return None
    for orig, repl in ESCAPES:
        s = s.replace(orig, repl)
    return s


def fqn(schema, table):
    return '%s.%s' % (schema, table)


def insert_line(cursor, fulltable, values):
    sorted_keys = sorted(values.keys())
    sql_columns = ', '.join(sorted_keys)
    sql_values = ', '.join(['%s'] * len(sorted_keys))
    sql = 'INSERT INTO %s (%s) VALUES (%s)' % (fulltable, sql_columns, sql_values)
    cursor.execute(sql, [values[k] for k in sorted_keys])


def delete_line(cursor, fulltable, keys):
    sorted_keys = sorted(keys.keys())
    sql = 'DELETE FROM %s' % (fulltable,)
    sql += ' WHERE ' + ' AND '.join('%s%s%%s' % (k, ' IS ' if keys[k] is None else ' = ') for k in sorted_keys)
    cursor.execute(sql, [keys[k] for k in sorted_keys])

## End mbslave code.


p_minus = re.compile('-[0-9]+')
p_plus = re.compile('\+[0-9]+')

if len(sys.argv) < 2:
    print "Usage: %s <table> <diff file>" % sys.argv[0]
    sys.exit(-1)

DIFFS = sys.argv[1:]

for diff in DIFFS:
    f = codecs.open(diff, 'r', 'utf-8')
    if not f:
        print "cannot open diff file"
        sys.exit(-1)

    fulltable = os.path.splitext(os.path.basename(diff))[0]
    cursor = old_db.cursor()
    while True:
        line = f.readline()
        if not line:
            break

        line = line.rstrip('\n')
        if not line:
            continue

        if not (p_minus.match(line) or p_plus.match(line)):
            continue

        columns = line.split('\t')
        columns[0] = columns[0][1:]  # remove minus or plus

        if columns[0].startswith('SELECT pg_catalog.setval'):
            continue

        if p_minus.match(line):
            keys = {}
            for pk in REPLICATED_TABLES[fulltable]:
                column_name, column_position, data_type, is_nullable, constraint_type = pk
                if constraint_type == "PRIMARY KEY":
                    keys[column_name] = unescape(columns[column_position - 1])
            delete_line(cursor, fulltable, keys)

        if p_plus.match(line):
            values = {}
            for pk in REPLICATED_TABLES[fulltable]:
                column_name, column_position, data_type, is_nullable, constraint_type = pk
                values[column_name] = unescape(columns[column_position - 1])
            insert_line(cursor, fulltable, values)

    cursor.close()


f.close()
old_db.commit()
