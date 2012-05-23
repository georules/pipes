#!/usr/bin/python
import sys
import subprocess

def main():
	if (len(sys.argv) < 2):
		exit("Need pipes");
	pipedir = sys.argv[1]
	pipefile = pipedir + "pipes"
	pipes = open(pipefile)
	pipelist = []
	for p in pipes:
		pipelist.append(makepipe(pipedir, p))
	for p in pipelist:
		print "Running " + str(p)
		runpipe(p)

def runpipe(pipe):
	ifile = pipe.location + pipe.input.data
	pfile,plang = determineprocessor(pipe.location + pipe.process.data)
	ofile = pipe.location + pipe.output.data
	exe = "/usr/bin/" + plang
	indata = open(ifile)
	datain = ""
	for d in indata:
		datain+=d
	p = subprocess.Popen([exe, pfile], stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
	out = p.communicate(input = datain)
	p.wait()
	o = open(ofile,'w')
	o.write(out[0]+out[1])
	o.close()
	 
def determineprocessor(p):
	ps = p.split(',')
	return ps[0],ps[1]

def makepipe(pipedir, line):
	tokenlist=[]
	line = line.replace(" ","")
	tokens = line.split('>')
	for t in tokens:
		data = t[t.find('(')+1:t.find(')')]
		tokenlist.append(token(t[0],data))
	return pipe(pipedir, tokenlist[0],tokenlist[1],tokenlist[2])

class pipe:
	def __init__(self, l, i, p, o):
		self.location = l
		self.input = i
		self.process = p
		self.output = o
	def __str__(self):
		i = str(self.input)
		p = str(self.process)
		o = str(self.output)
		l = self.location
		return "Pipe " + l + ": " + i + " > " + p + " > " + o

class token:
	def __init__(self, action, data):
		self.action = action
		self.data = data
	def __str__(self):
		return "Action:" + self.action + " Data:" + self.data

main()
