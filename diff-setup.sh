#!/bin/bash

OLD_DB=$1
NEW_DB=$2
TABLE=$3
OUT_DIR=$4

pg_dump -U musicbrainz -h musicbrainz_old_db -t $TABLE -a -f /tmp/$TABLE-old.sql $OLD_DB
pg_dump -U musicbrainz -h musicbrainz_old_db -t $TABLE -a -f /tmp/$TABLE-new.sql $NEW_DB
sort /tmp/$TABLE-old.sql > /tmp/$TABLE-old-sorted.sql
sort /tmp/$TABLE-new.sql > /tmp/$TABLE-new-sorted.sql
diff -Naur /tmp/$TABLE-old-sorted.sql /tmp/$TABLE-new-sorted.sql > /tmp/$TABLE.diff
./table-diff $TABLE /tmp/$TABLE.diff > $OUT_DIR/$TABLE.sql

rm -f /tmp/$TABLE-old.sql /tmp/$TABLE-new.sql /tmp/$TABLE-old-sorted.sql /tmp/$TABLE-new-sorted.sql 