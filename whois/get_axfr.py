#!/usr/bin/python
import dns.query
import dns.zone
import time

def get_axfr(zone_name):
	axfr_query = dns.query.xfr('127.0.0.1', zone_name)
	try:
		zones = dns.zone.from_xfr(axfr_query)
	except dns.exception.FormError:
		print "Format error...."
		return False

	output = "; Zone data for %s\n" % zone_name
	output += "; Generated @ %s\n" % time.strftime("%d/%m/%Y %H:%M")
	output += "; %d records\n" % len(zones.nodes.keys())

	for record in zones.nodes.keys():
		output += zones.nodes[record].to_text(record)
		output += "\n"

	return output

print get_axfr('damian.internal')
