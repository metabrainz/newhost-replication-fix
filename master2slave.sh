#!/bin/bash

psql -U musicbrainz_user -c 'TRUNCATE dbmirror_Pending CASCADE' musicbrainz_old_db
psql -U musicbrainz_user -c 'TRUNCATE dbmirror_PendingData CASCADE' musicbrainz_old_db
psql -U musicbrainz_user -f sql/caa/DropReplicationTriggers.sql musicbrainz_old_db
psql -U musicbrainz_user -f sql/documentation/DropReplicationTriggers.sql musicbrainz_old_db
psql -U musicbrainz_user -f sql/DropReplicationTriggers.sql musicbrainz_old_db
psql -U musicbrainz_user -f sql/statistics/DropReplicationTriggers.sql musicbrainz_old_db
psql -U musicbrainz_user -f sql/wikidocs/DropReplicationTriggers.sql musicbrainz_old_db
psql -U postgres -f sql/DropReplicationFunction.sql musicbrainz_old_db
