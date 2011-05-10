#!/usr/bin/env perl
use strict;
use Net::DNS;

my $res  = Net::DNS::Resolver->new;
$res->nameservers("127.0.0.1");

my @zone = $res->axfr("damian.internal");
if (@zone) {
	my $zone_output = "";

	$zone_output .= "; Generated at " . localtime . "\n";
	foreach my $rr (@zone) {
		my $record = $rr->string;
		$zone_output .= $record . "\n";
	}

	print $zone_output;
} else {
	print 'Zone transfer failed: ', $res->errorstring, "\n";
}
