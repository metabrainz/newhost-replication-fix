#!/usr/bin/env python

OLD_DB = "musicbrainz_old_db"
NEW_DB = "musicbrainz_new_db"
OUT_DIR = "out"

REPLICATED_TABLES = [ "alternative_medium"
    "alternative_medium_track",
    "alternative_release",
    "alternative_release_type",
    "alternative_track",
    "annotation",
    "area",
    "area_alias",
    "area_alias_type",
    "area_annotation",
    "area_gid_redirect",
    "area_tag",
    "area_type",
    "artist",
    "artist_alias",
    "artist_alias_type",
    "artist_annotation",
    "artist_credit",
    "artist_credit_name",
    "artist_gid_redirect",
    "artist_ipi",
    "artist_isni",
    "artist_meta",
    "artist_tag",
    "artist_type",
    "cdtoc",
    "cdtoc_raw",
    "country_area",
    "editor_collection_type",
    "event",
    "event_alias",
    "event_alias_type",
    "event_annotation",
    "event_gid_redirect",
    "event_meta",
    "event_tag",
    "event_type",
    "gender",
    "instrument",
    "instrument_alias",
    "instrument_alias_type",
    "instrument_annotation",
    "instrument_gid_redirect",
    "instrument_tag",
    "instrument_type",
    "iso_3166_1",
    "iso_3166_2",
    "iso_3166_3",
    "isrc",
    "iswc",
    "l_area_area",
    "l_area_artist",
    "l_area_event",
    "l_area_instrument",
    "l_area_label",
    "l_area_place",
    "l_area_recording",
    "l_area_release",
    "l_area_release_group",
    "l_area_series",
    "l_area_url",
    "l_area_work",
    "l_artist_artist",
    "l_artist_event",
    "l_artist_instrument",
    "l_artist_label",
    "l_artist_place",
    "l_artist_recording",
    "l_artist_release",
    "l_artist_release_group",
    "l_artist_series",
    "l_artist_url",
    "l_artist_work",
    "l_event_event",
    "l_event_instrument",
    "l_event_label",
    "l_event_place",
    "l_event_recording",
    "l_event_release",
    "l_event_release_group",
    "l_event_series",
    "l_event_url",
    "l_event_work",
    "l_instrument_instrument",
    "l_instrument_label",
    "l_instrument_place",
    "l_instrument_recording",
    "l_instrument_release",
    "l_instrument_release_group",
    "l_instrument_series",
    "l_instrument_url",
    "l_instrument_work",
    "l_label_label",
    "l_label_place",
    "l_label_recording",
    "l_label_release",
    "l_label_release_group",
    "l_label_series",
    "l_label_url",
    "l_label_work",
    "l_place_place",
    "l_place_recording",
    "l_place_release",
    "l_place_release_group",
    "l_place_series",
    "l_place_url",
    "l_place_work",
    "l_recording_recording",
    "l_recording_release",
    "l_recording_release_group",
    "l_recording_series",
    "l_recording_url",
    "l_recording_work",
    "l_release_group_release_group",
    "l_release_group_series",
    "l_release_group_url",
    "l_release_group_work",
    "l_release_release",
    "l_release_release_group",
    "l_release_series",
    "l_release_url",
    "l_release_work",
    "l_series_series",
    "l_series_url",
    "l_series_work",
    "l_url_url",
    "l_url_work",
    "l_work_work",
    "label",
    "label_alias",
    "label_alias_type",
    "label_annotation",
    "label_gid_redirect",
    "label_ipi",
    "label_isni",
    "label_meta",
    "label_tag",
    "label_type",
    "language",
    "link",
    "link_attribute",
    "link_attribute_credit",
    "link_attribute_text_value",
    "link_attribute_type",
    "link_creditable_attribute_type",
    "link_text_attribute_type",
    "link_type",
    "link_type_attribute_type",
    "medium",
    "medium_cdtoc",
    "medium_format",
    "medium_index",
    "orderable_link_type",
    "place",
    "place_alias",
    "place_alias_type",
    "place_annotation",
    "place_gid_redirect",
    "place_tag",
    "place_type",
    "recording",
    "recording_alias",
    "recording_alias_type",
    "recording_annotation",
    "recording_gid_redirect",
    "recording_meta",
    "recording_tag",
    "release",
    "release_alias",
    "release_alias_type",
    "release_annotation",
    "release_country",
    "release_gid_redirect",
    "release_group",
    "release_group_alias",
    "release_group_alias_type",
    "release_group_annotation",
    "release_group_gid_redirect",
    "release_group_meta",
    "release_group_primary_type",
    "release_group_secondary_type",
    "release_group_secondary_type_join",
    "release_group_tag",
    "release_label",
    "release_meta",
    "release_packaging",
    "release_raw",
    "release_status",
    "release_tag",
    "release_unknown_country",
    "replication_control",
    "script",
    "series",
    "series_alias",
    "series_alias_type",
    "series_annotation",
    "series_gid_redirect",
    "series_ordering_type",
    "series_tag",
    "series_type",
    "tag",
    "track",
    "track_gid_redirect",
    "track_raw",
    "url",
    "url_gid_redirect",
    "work",
    "work_alias",
    "work_alias_type",
    "work_annotation",
    "work_attribute",
    "work_attribute_type",
    "work_attribute_type_allowed_value",
    "work_gid_redirect",
    "work_meta",
    "work_tag",
    "work_type",
]

for table in REPLICATED_TABLES:
    subprocess.call(["diff-setup.sh", OLD_DB, NEW_DB, table, OUT_DIR])