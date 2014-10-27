# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
import subprocess
import threading
import os
import time
import codecs
# start_urls = [url.strip() for url in open('part_00000_urls.txt').readlines()]
def kill_lynx(pid):
	os.kill(pid, signal.SIGKILL)
	os.waitpid(-1, os.WNOHANG)
	print("lynx killed")

for i in range(3,4):
	infn = 'part-%05d' %(i)
	inputfile = open(infn)
	outfn = infn + '-namemap'
	outputfile = codecs.open(outfn,encoding='utf-8', mode='w+')
	linenum = 1
	for line in inputfile.readlines():
		url = line.split("\t")[0].decode('utf-8')
		print url
		cmd = "lynx -source " + url
		print cmd
		lynx = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
		# t = threading.Timer(300.0, kill_lynx, args=[lynx.pid])
		# t.start()
		file_data = lynx.stdout.read()
		# t.cancel()
		if file_data == '':
			outputfile.write(str(linenum) + "," + url + "," + " " + "," + " " + "," + " " + "\n")
			linenum += 1
			continue
		sel = Selector(text=file_data)
		fullnamelist = sel.xpath("/html/head/title/text()").extract()
		if len(fullnamelist) == 0:
			outputfile.write(str(linenum) + "," + url + "," + " " + "," + " " + "," + " " + "\n")
			linenum += 1
			continue
		fullnamelist = fullnamelist[0].split("|")[0].split(",")[0].split()
		# fullnamelist = sel.xpath("//span[@class = 'full-name']//text()").extract()
		fullname = " ".join(fullnamelist)
		lastname = fullnamelist[-1]
		firstname = " ".join(fullnamelist[:-1])
		outputfile.write(str(linenum) + "," + url + "," + fullname + "," + firstname + "," + lastname + "\n")
		# outputfile.flush()
		linenum += 1
	outputfile.close()

