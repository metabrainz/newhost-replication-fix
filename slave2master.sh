#!/bin/bash

psql -U postgres -f sql/CreateReplicationFunction.sql musicbrainz_old_db
psql -U musicbrainz_user -f sql/caa/CreateReplicationTriggers.sql musicbrainz_old_db
psql -U musicbrainz_user -f sql/CreateReplicationTriggers.sql musicbrainz_old_db
psql -U musicbrainz_user -f sql/documentation/CreateReplicationTriggers.sql musicbrainz_old_db
psql -U musicbrainz_user -f sql/statistics/CreateReplicationTriggers.sql musicbrainz_old_db
psql -U musicbrainz_user -f sql/wikidocs/CreateReplicationTriggers.sql musicbrainz_old_db
psql -U musicbrainz_user -c 'TRUNCATE dbmirror_Pending CASCADE' musicbrainz_old_db
psql -U musicbrainz_user -c 'TRUNCATE dbmirror_PendingData CASCADE' musicbrainz_old_db
