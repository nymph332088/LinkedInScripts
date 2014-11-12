# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# import re

# def findWholeWord(w):
#     return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

# namelist = [' '.join(x.split('" "')).strip() for x in open('stnames.txt','rb').readlines()]
# wholenamelist = [(i,ln,x.split(',')[2],x.split(',')[1]) for i in range(0,10) for ln, x in enumerate(open('part-%05d-namemap' %(i),'rb').readlines())]


# outfn = open('mapping_results.csv','wb')
# outfn.write('Index,STName,NumMT,MTResults\n')
# for nn, name in enumerate(namelist):
# 	fname = name.split()[0]
# 	lname = name.split()[-1]
# 	sresults = [(str(fn),str(ln), fullname, link) for fn, ln, fullname,link in wholenamelist if findWholeWord(fname)(fullname) and findWholeWord(lname)(fullname)]
# 	resultsstr = ":".join([";".join(l) for l in sresults])
# # 	print len(sresults)
# 	outfn.write(str(nn) + ","  + name + "," + str(len(sresults)) + "," + resultsstr + "\n")

# nummt = np.array([int(float(x.split(",")[2])) for linenum,x in enumerate(open('mapping_results.csv','rb').readlines()) if linenum != 0])

# mtresults = [x.split(",")[] for linenum,x in enumerate(open('mapping_results.csv','rb').readlines()) if linenum != 0]

# majors = {x.split(',')[j]:x.split(',')[j+2] for linenum, x in enumerate(open('majors.csv','rb').readlines()) \
#           for j in range(0,len(x.split(','))) if linenum != 0 and (j%4 ==0 or j%4 == 1)}
# del majors['']
# del majors['0']
# len(majors)
# f = open('majordict','wb')
# for key in majors:
# 	f.write(key +','+ majors[key] + '\n')

# <codecell>

from operator import itemgetter 
from collections import OrderedDict

b = [0,3,4,5,6,9]
f = open('../studentInfo4.csv','wb')
f.write(','.join(['FAT','Gender', 'ID', 'Entry_Major', 'Math_SAT', 'Verbal_SAT', 'SAT', \
         'GPA', 'Transfer_or_not', 'Graduated_or_not', 'GradMj_Reported',\
         'GradMj_Extracted', 'EndMj', 'Unique_Majors', 'Semesters_Enrolled', 'All_majors\n']))
for linenum,x in enumerate(open('../CSTmia10.csv','rb').readlines()):
    if linenum == 0:
#         header = x.split(',')
        continue
    
    if x.split(',')[1] == 'T':
        fat = 0
    elif  x.split(',')[1] == 'F':
        fat = 1
    else: 
        fat = 2
    
    gender = 0
    if x.split(',')[2] == 'F':
        gender = 1
    
    front = list(itemgetter(*b)(x.split(','))) #Front include the GPA, SAT and so on.
#     majorsSem = {sem + 1:cur for sem, cur in enumerate(x.split(',')[11:59]) if cur != '' and cur != 'GRADUATE' and cur != 'TRANSFER'}
# #     majorsSem = sorted(majorsSem.items(), key = itemgetter(0))
    
#     majors = [major for major in majorsSem]
#     semesters = [sem for sem,major in majorsSem]
    
    majors = []
    semesters = []
    [majors.append(cur) for cur in x.split(',')[11:59] if cur != '' and cur != 'GRADUATE' and cur != 'TRANSFER']
    [semesters.append(str(sem+1)) for sem, cur in enumerate(x.split(',')[11:59]) if cur != '' and cur != 'GRADUATE' and cur != 'TRANSFER']
    uqmajors = list(OrderedDict.fromkeys(majors))
    
    transfer = 0
    if 'TRANSFER' in x:
        transfer = 1
    
    graduate = 0
    if 'GRADUATE' in x:
        graduate = 1

    # header = list(itemgetter(*b)(header)).append([',','TRANSFER', 'Majors'])
    if (len(majors) == 0) or (not graduate):
        gradmajor = ''
    else:
        gradmajor = majors[-1]
    
    if len(majors) == 0:
        endmajor = ''
    else:
        endmajor = majors[-1]
    
    f.write( str(fat) + ','+ str(gender) + ',' + ','.join(front) + ',' + str(transfer) + ',' +\
        str(graduate) + ',' + str(x.split(',')[59]) + ',' + gradmajor + ',' + \
        endmajor + ',' + ';'.join(uqmajors) + ',' + ';'.join(semesters) + ',' + ';'.join(majors) + '\n')

