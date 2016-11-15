\set ON_ERROR_STOP 1
SET search_path = musicbrainz, public;

BEGIN;

CREATE FUNCTION "recordchange" () RETURNS trigger
AS '/usr/lib/postgresql/9.5/lib/pending.so', 'recordchange' LANGUAGE C;

COMMIT;
