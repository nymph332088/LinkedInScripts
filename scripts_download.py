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
import errno

for i in [2]:
	infn = 'part-%05d' %(i)
	inputfile = open(infn)
	linenum = 9013
# 	try:
# 		os.makedirs('part-' + str(i))
# 	except OSError as exception:
# 		if exception.errno != errno.EEXIST:
# 			raise
	for line in inputfile.readlines()[9012:9013]:
		outfn = 'part-' + str(i) + '/' +str(linenum)
		outputfile = codecs.open(outfn,encoding='utf-8', mode='w+')
		url = line.split("\t")[0].decode('utf-8')
		print url
		cmd = "lynx -source " + url
		print cmd
		lynx = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
		file_data = lynx.stdout.read().decode('utf-8')
		outputfile.write(file_data)
		linenum += 1
		outputfile.close()

