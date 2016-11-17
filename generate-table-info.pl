#!/usr/bin/perl

open(my $fh, '>', 'table_info.py');
print $fh "#!/usr/bin/env python\n\nREPLICATED_TABLES = {\n";

my $FIELDS = `psql --field-separator='\t' --file columns.sql --no-align --tuples-only --username musicbrainz musicbrainz_old_db`;
my @FIELDS = split "\n", $FIELDS;

for my $field (@FIELDS) {
    my ($schema, $table, $primary_keys) = split "\t", $field;

    $primary_keys =~ s/^{(.+)}$/(\1,)/;
    $primary_keys =~ s/{([^,]+),([^,]+),(True|False)}/("\1",\2,\3)/g;

    print $fh "\t\"$schema.$table\": $primary_keys,\n";
}

print $fh "}\n";
close $fh;
