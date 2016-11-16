#!/bin/bash

OLD_DB=$1
NEW_DB=$2
TABLE=$3

TMP=/tmp/newhost-replication-fix
mkdir -p $TMP

pg_dump -U postgres -t $TABLE -a -f $TMP/$TABLE-old.sql $OLD_DB
pg_dump -U postgres -t $TABLE -a -f $TMP/$TABLE-new.sql $NEW_DB
sort $TMP/$TABLE-old.sql > $TMP/$TABLE-old-sorted.sql
sort $TMP/$TABLE-new.sql > $TMP/$TABLE-new-sorted.sql

mkdir -p out
diff -Naur $TMP/$TABLE-old-sorted.sql $TMP/$TABLE-new-sorted.sql > out/$TABLE.diff
[ ! -s out/$TABLE.diff ] && rm -f out/$TABLE.diff

rm -rf "$TMP"
