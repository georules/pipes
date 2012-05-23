import cgi,urlparse,subprocess
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
rootdir = "/home/ubuntu/pipes/"
processor = "/home/ubuntu/pipe-proc/process.py"

def update_pipe(pipename):
	pipe = rootdir+pipename+"/"
	p = subprocess.Popen(["python", processor, pipe])

def get_pipe(pipename):
	update_pipe(pipename)
	cells = os.listdir(rootdir + pipename)
	pipes = []
	cells.sort()
	for c in cells:
		if c != "pipes":
			data = get_cell(rootdir+pipename, c)
			pipes.append([c,data])
	return pipes
	
def get_cell(pipename, cellname):
	filename = pipename+"/"+cellname
	data = ""
	for l in open(filename):
		data += l
	#data = "pipe:" + pipename + " cell: " + cellname + " filename: " +filename
	return data

def get_pipes():
	pipes = os.listdir(rootdir)
	pipes.sort()
	return pipes

class HTTPHandler(BaseHTTPRequestHandler):
	def start(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
	def show_debug(self):
		self.wfile.write(str(self.path)+"<br/>"+str(self.headers)+"<br/>")
	def show_pipe(self):
		pass
	def show_pipes(self):
		self.wfile.write(str(get_pipes()))
	def get_query(self):
		self.get = {}
		q = self.path.split('?',1)
		if(len(q) > 1):
			query = q[1]
			self.get = urlparse.parse_qs(query)
	def do_GET(self):
		try:
			self.start()
			self.get_query()
			keys = self.get.keys()
			if("debug" in keys):
				self.show_debug()
			if("pipe" in keys):
				request = self.get["pipe"][0]
				pipes = get_pipe(request)
				for p in pipes:
					self.wfile.write('<pre id="'+p[0]+'">'+p[1]+"</pre>")
			else:
				self.show_pipes()

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)
     
	def do_POST(self):
		try:
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				query=cgi.parse_multipart(self.rfile, pdict)
			self.send_response(301)
			self.end_headers()
			upfilecontent = query.get('upfile')
			#print "filecontent", upfilecontent[0]
			self.wfile.write("<HTML>POST OK.<BR><BR>");
			#self.wfile.write(upfilecontent[0]);    
		except:
			self.send_error(500,'Internal Server Error')

def main():
    try:
        server = HTTPServer(('', 80), HTTPHandler)
        print 'HTTP Server Started'
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()

main()
