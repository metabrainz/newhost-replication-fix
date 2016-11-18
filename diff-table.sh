#!/bin/bash

OLD_DB=$1
NEW_DB=$2
TABLE=$3

TMP=/tmp/newhost-replication-fix
mkdir -p $TMP

pg_dump -U postgres -t $TABLE -a $OLD_DB | ./dump-data.pl | sort > $TMP/$TABLE-old.sql
pg_dump -U postgres -t $TABLE -a $NEW_DB | ./dump-data.pl | sort > $TMP/$TABLE-new.sql

mkdir -p out
diff -Naur $TMP/$TABLE-old.sql $TMP/$TABLE-new.sql > out/$TABLE.diff
[ ! -s out/$TABLE.diff ] && rm -f out/$TABLE.diff

rm -rf "$TMP"
