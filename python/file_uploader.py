#!/usr/bin/env python
import httplib
import mimetypes
import os
import sys
import hashlib
import base64

SERVER = "stuff.damianzaremba.co.uk"
PUBLISH_PATH = "/doupload"
KEY = "meep"

BOUNDARY = 'h4ck0rzf7w'
CRLF = '\r\n'

def upload_file(file_path):
	if not os.path.isfile(file_path):
		print "Invalid file\n"
		sys.exit(5)

	file_name = os.path.basename(file_path)
	file_content = open(file_path, "rb").read()
	
	body = []
	body.append("--" + BOUNDARY)
	body.append('Content-Disposition: form-data; name="upload"')
	body.append('')
	body.append('')
	
	body.append("--" + BOUNDARY)
	body.append('Content-Disposition: form-data; name="file"')
	body.append('')
	body.append(file_name)
	
	body.append("--" + BOUNDARY)
	body.append('Content-Disposition: form-data; name="key"')
	body.append('')
	body.append(hashlib.sha1(KEY + str(len(file_name))).hexdigest())

	body.append("--" + BOUNDARY)
	body.append('Content-Disposition: file; filename="%s"' % (file_name))
	body.append('Content-Type: %s' % file_content_type(file_name))
	body.append('')
	body.append(file_content)
	
	body.append("--" + BOUNDARY + "--")
	body.append('')
	
	post_data = CRLF.join(body)
	
	request = httplib.HTTP(SERVER)
	request.putrequest('POST', PUBLISH_PATH)
	request.putheader('Host', SERVER)
	request.putheader('Content-type', 'multipart/form-data; boundary=%s' % BOUNDARY)
	request.putheader('Content-length', str(len(post_data)))
	request.endheaders()
	request.send(post_data)

	errcode, errmsg, headers = request.getreply()
	if errcode != 200:
		print errcode
		print errmsg
		return False
	else:
		return request.file.read()
	
def file_content_type(file_name):
	return mimetypes.guess_type(file_name)[0] or 'application/octet-stream'

if __name__ == "__main__":
	try:
		file = sys.argv[1]
	except IndexError:
		print "No file specified\n"
	else:
		files = sys.argv[1:]
		for file in files:
			print "Processing %s" % (file)
			result = upload_file(file)
			if result == False:
				print "Error occurred when talking to the server\n"
			else:
				if "[ERROR]" in result:
					print result
				elif "[OK]" in result:
					print result
				else:
					print "Unknown status returned\n"
