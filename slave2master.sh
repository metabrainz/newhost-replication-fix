#!/bin/bash

USER="$1"
DBNAME="$2"

psql -U postgres -f sql/CreateReplicationFunction.sql "$DBNAME"
psql -U "$USER" -f sql/caa/CreateReplicationTriggers.sql "$DBNAME"
psql -U "$USER" -f sql/CreateReplicationTriggers.sql "$DBNAME"
psql -U "$USER" -f sql/documentation/CreateReplicationTriggers.sql "$DBNAME"
psql -U "$USER" -f sql/statistics/CreateReplicationTriggers.sql "$DBNAME"
psql -U "$USER" -f sql/wikidocs/CreateReplicationTriggers.sql "$DBNAME"
psql -U "$USER" -c 'TRUNCATE dbmirror_Pending CASCADE' "$DBNAME"
psql -U "$USER" -c 'TRUNCATE dbmirror_PendingData CASCADE' "$DBNAME"
