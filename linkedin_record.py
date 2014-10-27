# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt

# <codecell>

i = 0
fn = 129
text = ''.join(open('part-%d/%d' %(i,fn),'rb').readlines())
# print text
line = open('part-%05d' %i,'rb').readlines()[fn-1]
print line
sel = Selector(text=text)
print sel.xpath('//div[@class="profile-overview-content"]')
print Selector(text=text).xpath('string(//div[@class="profile-overview-content"]//span[@class="full-name"])').extract()[0]
sel = sel.xpath('//div[re:test(@id,"education-(\d+)-view")]')
print len(sel)
print sel[0].xpath('string(.//h4[@class= "summary fn org"])').extract()[0].strip()
print sel[0].xpath('string(.//span[@class="degree"])').extract()[0].strip()
print sel[0].xpath('string(.//span[@class="major"])').extract()[0].strip()
print sel[0].xpath('string(.//span[@class="education-date"])').extract()[0].split()[0]
print sel[0].xpath('string(.//span[@class="education-date"])').extract()[0].split()[-1]
converter = html2text.HTML2Text()
converter.ignore_links = True
print ','.join(filter(None, converter.handle(sel[0].extract()).split('\n')))
print sel[0].xpath('string(.)').extract()
print ','.join(filter(None, sel[0].xpath('.//text()').extract()[0].split('\n')))

# <codecell>

i = 0
fn = 1085

text = ''.join(open('part-%d/%d' %(i,fn),'rb').readlines())
# print text
line = open('part-%05d' %i,'rb').readlines()[fn-1]
print line
from scrapy.selector import Selector
import html2text
sel = Selector(text=text)
sel
# sel.css('.-header')
# sel.xpath('//div[@class="profile-overview-content"]')
print Selector(text=text).xpath('string(//div[@class="profile-header"]//span[@class="full-name"])').extract()[0]
sel = sel.xpath('//div[@id="profile-education"]//div[starts-with(@class,"position")]')
print sel[0].xpath('string(.//h3[@class= "summary fn org"])').extract()[0].strip()
print sel[0].xpath('string(.//h4[@class="details-education"]//span[@class="degree"])').extract()[0].strip()
print sel[0].xpath('string(.//h4[@class="details-education"]//span[@class="major"])').extract()[0].strip()
print sel[0].xpath('string(.//abbr[@class="dtstart"]//@title)').extract()[0].split('-')[0]
print sel[0].xpath('string(.//abbr[@class="dtend"]//@title)').extract()[0].split('-')[1]
print sel[0].xpath('string(.//p[@class="desc details-education"])').extract()[0].strip()
converter = html2text.HTML2Text()
converter.ignore_links = True
print ','.join(filter(None, converter.handle(sel[0].extract()).split('\n')))
print ','.join(filter(None, sel[0].xpath('string(.)').extract()[0].split('\n')))

# <codecell>

from scrapy.selector import Selector
for i in range(0,10):
# for i in [0]:
    infn = 'part-%05d' %(i)
    orig = open('part-%05d' %(i)).readlines()
    names = open('part-%05d-namemap' %(i)).readlines()
    assert(len(orig) == len(names))
#     outfn = infn + '-edudf'
#     outputfile = codecs.open(outfn,encoding='utf-8', mode='w+')
    linenum = 0
    edudf = pd.DataFrame()
    edudict = {}
    edudict['Index'] = []
    edudict['FullName'] = []
    edudict['FirstName'] = []
    edudict['LastName'] = []
    edudict['University'] = []
    edudict['Degree'] = []
    edudict['Major'] = []
    edudict['StartYear'] = []
    edudict['StartMonth'] = []
    edudict['EndYear'] = []
    edudict['EndMonth'] = []
    edudict['Desc'] = []
    edudict['Text'] = []
    
    for ln in range(0,len(orig)):
#     for ln in [128]:
#         print "%d, %d" %(i, ln)
        pro_file = ''.join(open('part-%d/%d' %(i,ln+1),'rb').readlines())
        sel = Selector(text=pro_file)
        if sel.xpath('//div[@class="profile-header"]'):
        # Template 1
            fullname = sel.xpath('string(//div[@class="profile-header"]//span[@class="full-name"])').extract()[0]
            firstname = sel.xpath('string(//div[@class="profile-header"]//span[@class="given-name"])').extract()[0]
            lastname = sel.xpath('string(//div[@class="profile-header"]//span[@class="family-name"])').extract()[0]
            education = sel.xpath('//div[@id="profile-education"]//div[starts-with(@class,"position")]')
            for edu in education:
#                 print ln
                edudict['Index'].append(ln)
                edudict['FullName'].append(fullname)
                edudict['FirstName'].append(firstname)
                edudict['LastName'].append(lastname)
                edudict['University'].append(edu.xpath('string(.//h3[@class= "summary fn org"])').extract()[0].strip())
                edudict['Degree'].append(edu.xpath('string(.//h4[@class="details-education"]//span[@class="degree"])').extract()[0].strip())
                edudict['Major'].append(edu.xpath('string(.//h4[@class="details-education"]//span[@class="major"])').extract()[0].strip())
                starttime = edu.xpath('string(.//abbr[@class="dtstart"]//@title)').extract()[0] 
                if starttime:
                    edudict['StartYear'].append(starttime.split('-')[0])
                    edudict['StartMonth'].append(starttime.split('-')[1])
                else:
                    edudict['StartYear'].append('')
                    edudict['StartMonth'].append('')
                    
                endtime = edu.xpath('string(.//abbr[@class="dtend"]//@title)').extract()[0]
                if endtime:
                    edudict['EndYear'].append(endtime.split('-')[0])
                    edudict['EndMonth'].append(endtime.split('-')[1])
                else:
                    edudict['EndYear'].append('')
                    edudict['EndMonth'].append('')
                edudict['Desc'].append(','.join(filter(None, \
                                    edu.xpath('string(.//p[@class="desc details-education"])').extract()[0].split('\n'))))
                edudict['Text'].append(','.join(filter(None, edu.xpath('string(.)').extract()[0].split('\n'))))
                
        elif sel.xpath('//div[@class="profile-overview-content"]'):
        # Template 2
            fullname = sel.xpath('string(//div[@class="profile-overview-content"]//span[@class="full-name"])').extract()[0]
            firstname = fullname.split()[0]
            lastname = ' '.join(fullname.split()[1:])
            education = sel.xpath('//div[re:test(@id,"education-(\d+)-view")]')
            for edu in education:
#                 print ln
                edudict['Index'].append(ln)
                edudict['FullName'].append(fullname)
                edudict['FirstName'].append(firstname)
                edudict['LastName'].append(lastname)
                edudict['University'].append(edu.xpath('string(.//h4[@class= "summary fn org"])').extract()[0].strip())
                edudict['Degree'].append(edu.xpath('string(.//span[@class="degree"])').extract()[0].strip())
                edudict['Major'].append(edu.xpath('string(.//span[@class="major"])').extract()[0].strip())
                duration = edu.xpath('.//span[@class="education-date"]//time')
#                 duration = edu.xpath('string(.//span[@class="education-date"])').extract()[0]
                if len(duration) == 2:
                    edudict['StartYear'].append(duration[0].xpath('string(.)').extract()[0].strip().split()[-1])
                    edudict['StartMonth'].append(1)
                    edudict['EndYear'].append(duration[1].xpath('string(.)').extract()[0].strip().split()[-1])
                    edudict['EndMonth'].append(12)
                elif len(duration) == 1:
                    edudict['StartYear'].append('')
                    edudict['StartMonth'].append('')
                    edudict['EndYear'].append(duration[0].xpath('string(.)').extract()[0].strip().split()[-1])
                    edudict['EndMonth'].append(12)
                else:
                    edudict['StartYear'].append('')
                    edudict['EndYear'].append('')
                    edudict['StartMonth'].append('')
                    edudict['EndMonth'].append('')
                edudict['Desc'].append('')
                converter = html2text.HTML2Text()
                converter.ignore_links = True
                edudict['Text'].append(','.join(filter(None, converter.handle(edu.extract()).split('\n'))))
        else:
        # No html page extracted
            schools = orig[ln].split('\t')[4].split()
            degrees = orig[ln].split('\t')[5].split()
            durations = orig[ln].split('\t')[6].split()
#             print schools, degrees, durations
#             print len(schools),len(degrees),len(durations)
            if (len(schools) != len(degrees)) or (len(schools) != len(durations)) or (len(degrees) != len(durations)):
#                 print 'Exception: fail to get the years and educations %d, file %d' %(i,ln)
                linenum += 1
            else:
#                 print ln
                for count in range(len(schools)):
                    edudict['Index'].append(ln)
                    edudict['FullName'].append('')
                    edudict['FirstName'].append('')
                    edudict['LastName'].append('')
                    edudict['University'].append(schools[count])
                    edudict['Degree'].append(degrees[count])
                    edudict['Major'].append('')
                    edudict['StartYear'].append(durations[count].split('_')[0])
                    edudict['StartMonth'].append(1)
                    edudict['EndYear'].append(durations[count].split('_')[-1])
                    edudict['EndMonth'].append(12)
                    edudict['Desc'].append('')
                    edudict['Text'].append(','.join([schools[count],degrees[count],durations[count]]))
    
    cols=['Index','FullName','FirstName','LastName','University','Major','Degree',\
                                'StartYear','StartMonth','EndYear','EndMonth',\
                                'Desc','Text']
    for name in cols:
        print len(edudict[name])
    
    edudf = pd.DataFrame(edudict)
    edudf.to_csv('part-%05d-education.csv' %i, sep='\t', index=False, encoding='utf-8', cols=cols)
    print linenum

# <codecell>

for i in range(0,10):
    infn = 'part-%05d' %(i)
    orig = open('part-%05d' %(i)).readlines()
    metaInfo = {}
    cols = ['Index','UserID','CurrPosition','Industry','CurrLocation','Skills','Hobbies','Num_of_Conn','Languages','Summary']
    inds = [0,1,2,3,11,12,13,14,15]
    j = 0
    for col in cols:
        if col == 'Index':
            metaInfo[col] = [ln for ln,x in enumerate(orig)]
        else:
            metaInfo[col] = [x.split('\t')[inds[j]] for x in orig]
            j +=1
    metaInfo = pd.DataFrame(metaInfo)
    metaInfo.to_csv('part-%05d-metainfo.csv' %i, encoding='utf-8',cols=cols,index=False,sep='\t')

# <codecell>

import re
i = 0
fn = 1
text = ''.join(open('part-%d/%d' %(i,fn),'rb').readlines())
# print text
line = open('part-%05d' %i,'rb').readlines()[fn-1]
print line
sel = Selector(text=text)
print sel.xpath('//div[@class="profile-overview-content"]')
print Selector(text=text).xpath('string(//div[@class="profile-overview-content"]//span[@class="full-name"])').extract()[0]
sel = sel.xpath('//div[re:test(@id,"experience-(\d+)-view")]')
print len(sel)
print sel[0].xpath('string(.//h4)').extract()[0].strip()
print sel[0].xpath('.//h5')[-1].xpath('string(.)').extract()[0].strip()
print sel[0].xpath('string(.//span[@class="locality"])').extract()[0].strip()
time = sel[0].xpath('.//span[@class="experience-date-locale"]//time') 

st = time[0].xpath('string(.)').extract()[0].split()
print st[-1]
if len(st) == 2:
    print st[0]
else:
    print 'January'
timestr = sel[0].xpath('.//span[@class="experience-date-locale"]').xpath('string(.)').extract()[0]
print timestr
print re.search("\((.*?)\)", timestr).group(1)
print sel[0].xpath('string(.//span[@class="experience-date-locale"])').extract()[0].split()[0]
print sel[0].xpath('string(.//span[@class="experience-date-locale"])').extract()[0].split()[-1]
converter = html2text.HTML2Text()
converter.ignore_links = True
print ','.join(filter(None,sel[0].xpath('string(.//p[@class="description"])').extract()[0].split('\n')))
# print ','.join(filter(None, converter.handle(sel[0].xpath('.//p[@class="description"]')[0].extract()).split('\n')))
# print ','.join(filter(None, converter.handle(sel[0].extract()).split('\n')))
# print sel[0].xpath('string(.)').extract()
# print ','.join(filter(None, sel[0].xpath('.//text()').extract()[0].split('\n')))

# <codecell>

i = 0
fn = 27
text = ''.join(open('part-%d/%d' %(i,fn),'rb').readlines())
# print text
line = open('part-%05d' %i,'rb').readlines()[fn-1]
print line
from scrapy.selector import Selector
import html2text
sel = Selector(text=text)
sel
# sel.css('.-header')
# sel.xpath('//div[@class="profile-overview-content"]')
print Selector(text=text).xpath('string(//div[@class="profile-header"]//span[@class="full-name"])').extract()[0]
sel = sel.xpath('//div[@id="profile-experience"]//div[starts-with(@class,"position")]')
print sel[0].xpath('string(.//span[@class="org summary"])').extract()[0].strip()
print sel[0].xpath('string(.//span[@class= "title"])').extract()[0].strip()
print ','.join(filter(None,sel[0].xpath('string(.//p[starts-with(@class," description")])').extract()[0].split('\n')))

print sel[0].xpath('string(.//abbr[@class="dtstart"]//@title)').extract()[0].split('-')[0]
# print sel[0].xpath('string(.//abbr[@class="dtend"]//@title)').extract()[0].split('-')[1]
converter = html2text.HTML2Text()
converter.ignore_links = True
# print ','.join(filter(None, converter.handle(sel[0].xpath('.//p[starts-with(@class," description")]')[0].extract()).split('\n')))

# <codecell>

from scrapy.selector import Selector
cols = ['Index','Company','Position','StartYear','StartMonth','EndYear','EndMonth','Duration','Location','Desc']
for i in range(1,10):
# for i in [0]:
    infn = 'part-%05d' %(i)
    orig = open('part-%05d' %(i)).readlines()
    names = open('part-%05d-namemap' %(i)).readlines()
    assert(len(orig) == len(names))
#     outfn = infn + '-edudf'
#     outputfile = codecs.open(outfn,encoding='utf-8', mode='w+')
    linenum = 0
    edudf = pd.DataFrame()
    edudict = {}
    for col in cols:
        edudict[col] = []
    
    for ln in range(0,len(orig)):
#     for ln in [0]:
#         print "%d, %d" %(i, ln)
        pro_file = ''.join(open('part-%d/%d' %(i,ln+1),'rb').readlines())
        sel = Selector(text=pro_file)
        if sel.xpath('//div[@class="profile-header"]'):
            # Template 1
            experience = sel.xpath('//div[@id="profile-experience"]//div[starts-with(@class,"position")]')
            for edu in experience: 
                edudict['Index'].append(ln)
                edudict['Company'].append(edu.xpath('string(.//span[@class="org summary"])').extract()[0].strip())
                edudict['Position'].append(edu.xpath('string(.//span[@class= "title"])').extract()[0].strip())

                starttime = edu.xpath('string(.//abbr[@class="dtstart"]//@title)').extract()[0] 
                if starttime:
                    edudict['StartYear'].append(starttime.split('-')[0])
                    try:
                        edudict['StartMonth'].append(starttime.split('-')[1])
                    except IndexError:
                        edudict['StartMonth'].append('')
                else:
                    edudict['StartYear'].append('')
                    edudict['StartMonth'].append('')

                endtime = edu.xpath('string(.//abbr[@class="dtend"]//@title)').extract()[0]
                if endtime:
                    edudict['EndYear'].append(endtime.split('-')[0])
                    try:
                        edudict['EndMonth'].append(endtime.split('-')[1])
                    except IndexError:
                        edudict['EndMonth'].append('')
                elif edu.xpath('string(.//abbr[@class="dtstamp"]//@title)').extract()[0]:
                    edudict['EndYear'].append(2014)
                    edudict['EndMonth'].append('')
                else:
                    edudict['EndYear'].append('')
                    edudict['EndMonth'].append('')
                edudict['Duration'].append(edu.xpath('string(.//span[@class="duration"])').extract()[0].strip())
                edudict['Location'].append(edu.xpath('string(.//span[@class="location"])').extract()[0].strip())
                desc = ','.join(filter(None,edu.xpath('string(.//p[starts-with(@class," description")])').extract()[0].split('\n')))
                edudict['Desc'].append(desc)
                
        elif sel.xpath('//div[@class="profile-overview-content"]'):
        # Template 2
#             fullname = sel.xpath('string(//div[@class="profile-overview-content"]//span[@class="full-name"])').extract()[0]
#             firstname = fullname.split()[0:1]
#             lastname = ' '.join(fullname.split()[1:])
            experience = sel.xpath('//div[re:test(@id,"experience-(\d+)-view")]')
            for edu in experience:
                edudict['Index'].append(ln)
                edudict['Company'].append(edu.xpath('.//h5')[-1].xpath('string(.)').extract()[0].strip())
                edudict['Position'].append(edu.xpath('string(.//h4)').extract()[0].strip())
                time = edu.xpath('.//span[@class="experience-date-locale"]//time') 
                try:
                    st = time[0].xpath('string(.)').extract()[0].split()
                except IndexError:
                    edudict['StartYear'].append('')
                    edudict['StartMonth'].append('')
                    edudict['EndYear'].append('')
                    edudict['EndMonth'].append('')
                else:
                    edudict['StartYear'].append(st[-1])
                    if len(st) == 2:
                        edudict['StartMonth'].append(st[0])
                    else:
                        edudict['StartMonth'].append('January')

                    if len(time) == 2:
                        end = time[1].xpath('string(.)').extract()[0].split()
                        edudict['EndYear'].append(end[-1])
                        if len(end) == 2:
                            edudict['EndMonth'].append(end[0])
                        else:
                            edudict['EndMonth'].append('December')
                    else:
                        edudict['EndYear'].append('Present')
                        edudict['EndMonth'].append('')
                
                timestr = edu.xpath('string(.//span[@class="experience-date-locale"])').extract()[0]
                
                match = re.search(r"\((.*?)\)", timestr)
                if match:
                    edudict['Duration'].append(match.group(1))
                else:
                    edudict['Duration'].append('')
                edudict['Location'].append(edu.xpath('string(.//span[@class="locality"])').extract()[0].strip())
                converter = html2text.HTML2Text()
                converter.ignore_links = True
                desc = ','.join(filter(None,edu.xpath('string(.//p[@class="description"])').extract()[0].split('\n')))
                edudict['Desc'].append(desc)
        else:
#                 print 'Exception: fail to get the years and educations %d, file %d' %(i,ln)
                linenum += 1
    for name in cols:
        print len(edudict[name])
    
    edudf = pd.DataFrame(edudict, columns= cols)
#     print edudf
    edudf.to_csv('part-%05d-experience.csv' %i, sep='\t', index=False, encoding='utf-8', cols=cols)
    print linenum

