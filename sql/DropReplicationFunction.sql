\set ON_ERROR_STOP 1
SET search_path = musicbrainz, public;

BEGIN;

DROP FUNCTION "recordchange" ();

COMMIT;
