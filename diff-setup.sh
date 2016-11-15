#!/bin/bash

OLD_DB=$1
NEW_DB=$2
TABLE=$3
OUT_DIR=$4

TMP=/tmp/newhost-replication-fix
mkdir -p $TMP

pg_dump -U musicbrainz_user -t $TABLE -a -f $TMP/$TABLE-old.sql $OLD_DB
pg_dump -U musicbrainz_user -t $TABLE -a -f $TMP/$TABLE-new.sql $NEW_DB
sort $TMP/$TABLE-old.sql > $TMP/$TABLE-old-sorted.sql
sort $TMP/$TABLE-new.sql > $TMP/$TABLE-new-sorted.sql

mkdir -p "$OUT_DIR"
diff -Naur $TMP/$TABLE-old-sorted.sql $TMP/$TABLE-new-sorted.sql > $OUT_DIR/$TABLE.diff
[ ! -s "$OUT_DIR/$TABLE.diff" ] && rm -f "$OUT_DIR/$TABLE.diff"

rm -rf "$TMP"
