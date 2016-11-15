#!/bin/bash

OLD_DB=$1
NEW_DB=$2
TABLE=$3
OUT_DIR=$4

TMP=/tmp/newhost-replication-fix
mkdir -p $TMP

pg_dump -U musicbrainz -t $TABLE -a -f $TMP/$TABLE-old.sql $OLD_DB
pg_dump -U musicbrainz -t $TABLE -a -f $TMP/$TABLE-new.sql $NEW_DB
sort $TMP/$TABLE-old.sql > $TMP/$TABLE-old-sorted.sql
sort $TMP/$TABLE-new.sql > $TMP/$TABLE-new-sorted.sql
diff -Naur $TMP/$TABLE-old-sorted.sql $TMP/$TABLE-new-sorted.sql > $TMP/$TABLE.diff

mkdir -p "$OUT_DIR"
./table-diff.py $TABLE $TMP/$TABLE.diff > "$OUT_DIR/$TABLE.sql"
[ ! -s "$OUT_DIR/$TABLE.sql" ] && rm -f "$OUT_DIR/$TABLE.sql"

rm -rf "$TMP"
