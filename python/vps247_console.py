#!/usr/bin/env python
import urlparse
import urllib
import urllib2
import json
import os
import sys
import random
import select
import socket

API_KEY = ""
PROXY_PORT = None

def api_call(url=''):
	url = 'http://admin.vps247.com%s' % url
	headers = {
		'x-vps247-api-key' : API_KEY,
		'Accept': 'application/json',
	}

	request = urllib2.Request(url, headers=headers)
	try:
		response = urllib2.urlopen(request)
	except urllib2.URLError, e:
		return (e.code, e.read())
	else:
		return (response.code, response.read())

def get_vms():
	(code, rdata) = api_call('/vms')
	if code != 200:
		return False

	vms = []
	data = json.loads(rdata)
	for vmd in data:
		vms.append(
			(vmd['vm']['id'], vmd['vm']['name'])
		)
	return vms

def get_console(vmid):
	(code, rdata) = api_call('/vms/%s/console' % vmid)
	if code != 200:
		return False

	data = json.loads(rdata)
	connect_session = data['session']
	connect_url = data['url']
	connect_url_parsed = urlparse.urlparse(connect_url)
	connect_url_qsl = urlparse.parse_qsl(connect_url_parsed.query)

	if not PROXY_PORT:
		proxy_server_port = random.randint(40000, 60000)
	else:
		proxy_server_port = PROXY_PORT

	vnc_client_port = connect_url_parsed.port
	if not vnc_client_port:
		vnc_client_port = 80

	try:
		proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		proxy_server.bind(('127.0.0.1', proxy_server_port))
		proxy_server.listen(1)
	except socket.error:
		print "Could not bind to 127.0.0.1:%d" % proxy_server_port
		return False

	vnc_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	vnc_client.connect((connect_url_parsed.netloc, vnc_client_port))

	connect_ref = ''
	for k, v in connect_url_qsl:
		if k == "ref":
			connect_ref = v

	connect_string = 'CONNECT %s?%s HTTP/1.1\r\n\r\n' % (
		connect_url_parsed.path,
		urllib.urlencode(
			{
				'ref': connect_ref,
				'session_id': connect_session,
			}
		)
	)

	vnc_client.send(connect_string)
	buffer = ''
	while "\r\n\r\n" not in buffer:
		buffer += vnc_client.recv(512)
	buffer = '\r\n\r\n'.join(buffer.split('\r\n\r\n')[1:])

	print "Proxy listening on port %s" % proxy_server_port
	inputs = [proxy_server, vnc_client]
	outputs = []
	running = True

	os.system('vncviewer localhost:%s &' % proxy_server_port)
	
	'''
	This is kinda messy as we only proxy a 1<>1 connection...
	Probably a better way of doing it but without using threads and buffers this just works.
	'''
	while running:
		inputready, outputready, exceptready = select.select(inputs, outputs, [])
		for s in inputready:
			if s == proxy_server:
				client, address = proxy_server.accept()
				print "Recieved connection from %s:%d" % address

				if len(outputs) > 0:
					print "Killing off %s:%d" % address
					client.close()
				else:
					inputs.append(client)
					outputs.append(client)
					client.send(buffer)
					buffer = ''
			elif s == vnc_client:
				data = s.recv(512)
				if data:
					if len(outputs) > 0:
						for o in outputs:
							o.send(buffer)
							o.send(data)
						buffer = ''
					else:
						buffer += data
				else:
					print "VNC client disconnected"
					running = False

					vnc_client.close()
					inputs.remove(vnc_client)

					for cs in inputs:
						if cs in [proxy_server, vnc_client]: continue # We handle these later
						try:
							cs.close()
						except:
							pass

						if cs in inputs:
							inputs.remove(cs)
						if cs in outputs:
							outputs.remove(cs)

					proxy_server.close()
			else:
				data = s.recv(1024)
				if data:
					vnc_client.send(data)
				else:
					s.close()
					inputs.remove(s)
					outputs.remove(s)
					if len(outputs) == 0:
						print "Last client left, exiting..."
						running = False
						vnc_client.close()
						proxy_server.close()

try:
	vmid = sys.argv[1]
except IndexError:
	vms = get_vms()
	if not vms:
		print "Could not get vms"
	else:
		print "ID\t\tName"
		print "--\t\t----"
		for vmid, vmname in vms:
			print "%s\t\t%s" % (vmid, vmname)
else:
	get_console(vmid)
