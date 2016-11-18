#!/usr/bin/env perl

while (<>) { last if $_ =~ /^COPY /; }
while (<>) { $_ =~ /^\\\./ ? exit 0 : print $_; }
