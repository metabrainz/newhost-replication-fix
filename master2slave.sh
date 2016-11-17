#!/bin/bash

USER="$1"
DBNAME="$2"

psql -U "$USER" -c 'TRUNCATE dbmirror_Pending CASCADE' "$DBNAME"
psql -U "$USER" -c 'TRUNCATE dbmirror_PendingData CASCADE' "$DBNAME"
psql -U "$USER" -f sql/caa/DropReplicationTriggers.sql "$DBNAME"
psql -U "$USER" -f sql/documentation/DropReplicationTriggers.sql "$DBNAME"
psql -U "$USER" -f sql/DropReplicationTriggers.sql "$DBNAME"
psql -U "$USER" -f sql/statistics/DropReplicationTriggers.sql "$DBNAME"
psql -U "$USER" -f sql/wikidocs/DropReplicationTriggers.sql "$DBNAME"
psql -U postgres -f sql/DropReplicationFunction.sql "$DBNAME"
