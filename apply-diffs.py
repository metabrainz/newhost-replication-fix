#!/usr/bin/env python

import pprint
import codecs
import os
import os.path
import psycopg2
import re
import sys
import tarfile
from table_info import REPLICATED_TABLES


if len(sys.argv) < 4:
    print "Usage: %s <user> <database> <table> <diff files>" % sys.argv[0]
    sys.exit(-1)


old_db = psycopg2.connect('user=%s dbname=%s host=127.0.0.1 port=5432' % (sys.argv[1], sys.argv[2]))


def fqn(schema, table):
    return '%s.%s' % (schema, table)


COLUMN_INFO = {}
for table, columns in REPLICATED_TABLES.iteritems():
    for column in columns:
        COLUMN_INFO[fqn(table, column[0])] = column[1:]


# Used to keep track of changes to rows (read: primary keys) in all replication
# packets found in the subtract/ dir. These changes will be excluded from the
# overall diff.
PACKET_CHANGES = {}


## Code adapted from mbslave with some modifications.
## Copyright (C) 2010-2015  Lukas Lalinksy
## https://bitbucket.org/lalinsky/mbslave/raw/e86f415/mbslave-sync.py

def parse_data_fields(s):
    fields = {}
    for name, value in re.findall(r'''"([^"]+)"=('(?:''|[^'])*')? ''', s):
        if not value:
            value = None
        else:
            value = value[1:-1].replace("''", "'").replace("\\\\", "\\")
        fields[name] = value
    return tuple(sorted(fields.iteritems()))


def parse_bool(s):
    return s == 't'


ESCAPES = (('\\b', '\b'), ('\\f', '\f'), ('\\n', '\n'), ('\\r', '\r'),
           ('\\t', '\t'), ('\\v', '\v'), ('\\\\', '\\'))

def unescape(s):
    if s == '\\N':
        return None
    for orig, repl in ESCAPES:
        s = s.replace(orig, repl)
    return s


def read_psql_dump(fp, types):
    for line in fp:
        values = map(unescape, line.rstrip('\r\n').split('\t'))
        for i, value in enumerate(values):
            if value is not None:
                values[i] = types[i](value)
        yield values


def parse_name(table):
    if '.' in table:
        schema, table = table.split('.', 1)
    else:
        schema = 'musicbrainz'
    schema = schema.strip('"')
    table = table.strip('"')
    return schema, table


def insert_line(cursor, fulltable, values):
    sql_columns = ', '.join(i[0] for i in values)
    sql_values = ', '.join(['%s'] * len(values))
    sql = 'INSERT INTO %s (%s) VALUES (%s)' % (fulltable, sql_columns, sql_values)
    cursor.execute(sql, [i[1] for i in values])


def delete_line(cursor, fulltable, keys):
    sql = 'DELETE FROM %s' % (fulltable,)
    sql += ' WHERE ' + ' AND '.join('%s%s%%s' % (i[0], ' IS ' if i[1] is None else ' = ') for i in keys)
    cursor.execute(sql, [i[1] for i in keys])


class PacketImporter(object):

    def __init__(self):
        self._data = {}
        self._transactions = {}

    def load_pending_data(self, fp):
        dump = read_psql_dump(fp, [int, parse_bool, parse_data_fields])
        for id, key, values in dump:
            self._data[(id, key)] = values

    def load_pending(self, fp):
        dump = read_psql_dump(fp, [int, str, str, int])
        for id, table, type, xid in dump:
            schema, table = parse_name(table)
            transaction = self._transactions.setdefault(xid, [])
            transaction.append((id, schema, table, type))

    def process(self):
        for xid in sorted(self._transactions.keys()):
            transaction = self._transactions[xid]
            for id, schema, table, type in sorted(transaction):
                fulltable = fqn(schema, table)
                keys = self._data.get((id, True), tuple())
                # keys are only available for updates and deletes.
                if type == 'i':
                    values = self._data.get((id, False), tuple())
                    keys = tuple(v for v in values if COLUMN_INFO[fqn(fulltable, v[0])][1])
                PACKET_CHANGES.setdefault(fulltable, {}).setdefault(keys, set()).add(type)


def process_tar(fname):
    tar = tarfile.open(name=fname, mode='r:bz2', encoding='utf-8')
    importer = PacketImporter()
    for member in tar:
        if member.name in ('mbdump/Pending', 'mbdump/dbmirror_pending'):
            importer.load_pending(tar.extractfile(member))
        elif member.name in ('mbdump/PendingData', 'mbdump/dbmirror_pendingdata'):
            importer.load_pending_data(tar.extractfile(member))
    importer.process()


## End mbslave code.


p_minus = re.compile('-[0-9]+')
p_plus = re.compile('\+[0-9]+')

current_dir = os.path.dirname(os.path.abspath(__file__))
subtract_dir = os.path.join(current_dir, "subtract")

if os.path.isdir(subtract_dir):
    # subtract packets' sql in reverse order
    fnames = sorted(os.listdir(subtract_dir))
    for f in fnames:
        process_tar(os.path.join(subtract_dir, f))

print pprint.pprint(PACKET_CHANGES)

DIFFS = sys.argv[3:]

for diff in DIFFS:
    f = codecs.open(diff, 'r', 'utf-8')
    if not f:
        print "cannot open diff file"
        sys.exit(-1)

    skipped_deletes = {}
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

        if not (p_minus.match(line) or p_plus.match(line)):
            continue

        keys = {}
        values = {}
        for column_info in REPLICATED_TABLES[fulltable]:
            column_name, column_position, is_pkey = column_info
            values[column_name] = unescape(columns[column_position - 1])
            if is_pkey:
                keys[column_name] = values[column_name]

        keys = tuple(sorted(keys.iteritems()))

        packet_changes = PACKET_CHANGES.get(fulltable, {}).get(keys)
        if packet_changes:
            # If the entity was inserted, updated, or deleted in a later packet,
            # we can skip any changes to that entity (the end result will be
            # the same) UNLESS the entity was added in the full diff but not
            # in the later packets. (It must be created for later operations to
            # work.)
            if not (p_plus.match(line) and not 'i' in packet_changes):
                if p_minus.match(line):
                    print ('skipping DELETE', fulltable, keys)
                    # Since we only have -/+ in the diff, if we skip a deletion
                    # we have to skip the corresponding insertion too (because
                    # together they represent an UPDATE).
                    skipped_deletes.setdefault(fulltable, {})[keys] = True
                if p_plus.match(line):
                    print ('skipping INSERT', fulltable, keys)
                continue
            if p_plus.match(line) and keys in skipped_deletes.get(fulltable, {}):
                continue

        if p_minus.match(line):
            delete_line(cursor, fulltable, keys)

        if p_plus.match(line):
            values = tuple(sorted(values.iteritems()))
            insert_line(cursor, fulltable, values)

    cursor.close()


f.close()
old_db.commit()
