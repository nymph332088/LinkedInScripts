# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pylab as plt

# <codecell>

studentInfo = pd.read_csv('studentInfo4.csv',dtype=object)
print studentInfo.shape
majorDict = pd.read_csv('majordict.csv', dtype=object)
majorDict.index = majorDict.ID

# <codecell>

%pylab inline
width = 0.35
k = 20
StMj = studentInfo.Entry_Major
# StMj = StMj.value_counts().iloc[:k]
StMj = np.log2(StMj.value_counts().iloc[:k]+1)
EndMj = studentInfo.EndMj
# EndMj = EndMj.value_counts()
EndMj = np.log2(EndMj.value_counts()+1)

fig, ax = plt.subplots()
ind = np.arange(k)
rect1 = ax.bar(ind, StMj,width, color='r')
rect2 = ax.bar(ind+width, EndMj.ix[StMj.index],width, color='b')
labels = majorDict.ix[StMj.iloc[:k].index].Name
labels[pd.isnull(labels)] = labels[pd.isnull(labels)].index
plt.xticks(ind+2*width, labels, rotation = 45, ha='right')
ax.set_ylabel('Log2 Number of students')
plt.legend((rect1[0],rect2[0]),('EntryMajor','EndMajor'))
plt.gcf().tight_layout()
plt.savefig('pic/entrymajor_vs_endmajor.png')
# plt.set_xticks(ind + 0.5/2)
# ax.set_xticklabels(EndMj.iloc[:10].index)

# <codecell>

%pylab inline
width = 0.35
k = 20
StMj = studentInfo.EndMj
# StMj = StMj.value_counts().iloc[:k]
StMj = np.log2(StMj.value_counts().iloc[:k]+1)
EndMj = studentInfo.Entry_Major
# EndMj = EndMj.value_counts()
EndMj = np.log2(EndMj.value_counts()+1)

fig, ax = plt.subplots()
ind = np.arange(k)
rect1 = ax.bar(ind+width, StMj,width, color='b')
rect2 = ax.bar(ind, EndMj.ix[StMj.index],width, color='r')
labels = majorDict.ix[StMj.iloc[:k].index].Name
labels[pd.isnull(labels)] = labels[pd.isnull(labels)].index
plt.xticks(ind+2*width, labels, rotation = 45, ha='right')
ax.set_ylabel('Log2 Number of students')
plt.legend((rect2[0],rect1[0]),('EntryMajor','EndMajor'))
plt.gcf().tight_layout()
# plt.savefig('pic/entrymajor_vs_endmajor.png')
# plt.set_xticks(ind + 0.5/2)
# ax.set_xticklabels(EndMj.iloc[:10].index)

# <codecell>

st_mathced_Info = studentInfo[studentInfo.NumMT == '1']
st_mathced_Info.All_majors[pd.isnull(st_mathced_Info.All_majors)] = ''
allIdsInRecord = np.unique([y for x in st_mathced_Info.All_majors.values for y in x.split(';')])
totalIdsForMatch = majorDict.ix[allIdsInRecord].ID
missingIds = totalIdsForMatch[pd.isnull(totalIdsForMatch)].index

# <codecell>

mid_st_dict = {}
for id in missingIds:
    mid_st_dict[id] = [sind for sind in st_mathced_Info.index if id in st_mathced_Info.ix[sind].All_majors.split(';')]

# <codecell>

mjnmLinkin= {}
for key in mid_st_dict.keys():
    # 5th column in file
    mjnmLinkin[key] = []
    for st in mid_st_dict[key]:
        fn = int(float(st_mathced_Info.ix[st].MTResults.split(';')[0]))
        ln = int(float(st_mathced_Info.ix[st].MTResults.split(';')[1]))
        mjnmLinkin[key].append(open('part-%05d' %(fn),'rb').readlines()[ln].split('\t')[5])

# <codecell>

import csv
writer = csv.writer(open('missingmajor.csv', 'wb'))
for key, value in mjnmLinkin.items():
   writer.writerow([key, value])

# <codecell>

st_mathced_Info = studentInfo[studentInfo.NumMT == '1']
st_mathced_Info.shape

%pylab inline
width = 0.35
k = 20
StMj = studentInfo.EndMj
# StMj = StMj.value_counts().iloc[:k]
StMj = np.log2(StMj.value_counts().iloc[:k]+1)
EndMj = st_mathced_Info.EndMj
# EndMj = EndMj.value_counts()
EndMj = np.log2(EndMj.value_counts()+1)

fig, ax = plt.subplots()
ind = np.arange(k)
rect1 = ax.bar(ind, StMj,width, color='r')
rect2 = ax.bar(ind+width, EndMj.ix[StMj.index],width, color='b')
labels = majorDict.ix[StMj.iloc[:k].index].Name
labels[pd.isnull(labels)] = labels[pd.isnull(labels)].index
plt.xticks(ind+2*width, labels, rotation = 45, ha='right')
ax.set_ylabel('Log2 Number of students')
ax.set_xlabel('Top 20 final majors for overall and linkedin students') 
plt.legend((rect1[0],rect2[0]),('Overall','In LinkedIn'))
plt.gcf().tight_layout()
plt.savefig('pic/major_bias.png')
# plt.set_xticks(ind + 0.5/2)
# ax.set_xticklabels(EndMj.iloc[:10].index)

# <codecell>

import re
def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

# bioch_sts = []

# for i in range(0,10):
#     for ln, x in enumerate(open('part-%05d-namemap' %(i),'rb').readlines()):
#         major = x.split('\t')[5]
#         duration = x.split('\t')[6]
matched_st = [tuple(x.split(';')[:2]) for x in st_mathced_Info.MTResults]
names = ['biochemistry','pharmacy','biology', 'psychology','kinesiology','anthropology','nursing','marketing','accounting']        
results = {}
for name in names:
    linkin_st = [(str(i),str(ln)) for i in range(0,10)  for ln, x in enumerate(open('part-%05d' %(i),'rb').readlines())\
             if name in x.split('\t')[5].lower()]
    notmatched = [x for x in linkin_st if x not in matched_st]
    results[name] = [len(linkin_st),len(notmatched),len(linkin_st) - len(notmatched)]

# <codecell>

studentInfo = pd.read_csv('studentInfo5.csv',sep='\t')
studentInfo
print len(studentInfo)
education = [ pd.read_csv('part-%05d-education.csv' %i, sep='\t') for i in range(0,10)]
print len(education)
education = [edu[~pd.isnull(edu.FullName)] for edu in education]
for i, edu in enumerate(education):
    edu['File'] = np.zeros((len(edu),)) + i
education = pd.concat(education,axis=0)
print len(education)
templeStu = education[[bool(findWholeWord('temple')(uni)) for uni in  education.University]]
print len(templeStu.groupby(['File','Index']))
recordedStu = templeStu[(templeStu.StartYear.astype('float')<=2010) & (templeStu.StartYear.astype('float')>=1989)]
print len(recordedStu.groupby(['File','Index']))
recordedStu.Major[pd.isnull(recordedStu.Major)] = ''
recordedStu.Degree[pd.isnull(recordedStu.Degree)]= ''
bachelorStu = recordedStu
degrees = [''.join(x.split('.')) for x in bachelorStu.Degree]
masterOrPhD = []
for stdg in degrees:
    mas = False
    for dg in mst:
        if(findWholeWord(dg)(stdg)):
            mas = True
    masterOrPhD.append(mas)
bachelorStu = bachelorStu[~ np.array(masterOrPhD)]
print len(bachelorStu.groupby(['File','Index']))

# <codecell>

names = ['physics','math','mathematics','chemistry']
st_mathced_Info = studentInfo[studentInfo.NumMT != 0]
matched_st = [tuple(x.split(';')[:2]) for x in st_mathced_Info.MTResults]
recordedStu.Major[pd.isnull(recordedStu.Major)] = ''
recordedStu.Degree[pd.isnull(recordedStu.Degree)]= ''
results = {}
mst = ['master','MA', 'MS', 'MEd', 'MSc', 'MEB', 'MDes', 'MNCM', 'MSN', \
       'MSW', 'MPA', 'MPC', 'MPP','MPH', 'MC', 'MCA', 'MCouns', 'MLA', 'MLIS', 'MDiv', \
       'ALM', 'MiM', 'MBA', 'MBA Tech', 'MCom', 'MBus', 'MI', 'PSM', \
       'MEng', 'MMath', 'MPhys', 'MPsych', 'MSci', 'MChem', 'MBiol', 'MGeol','doctor','phd','ph d','dphi']
for name in names:
    isMajorMatch = [(bool(findWholeWord(name)(major)) or bool(findWholeWord(name)(degree))) and \
                    (not bool(findWholeWord('education')(major)))\
                    for (major,degree) in zip(recordedStu['Major'].values,recordedStu['Degree'].values)]
    majorStu = recordedStu[isMajorMatch]
    degrees = [''.join(x.split('.')) for x in majorStu.Degree]
    masterOrPhD = []
    for stdg in degrees:
        mas = False
        for dg in mst:
            if(findWholeWord(dg)(stdg)):
                mas = True
        masterOrPhD.append(mas)
    majorStu = majorStu[~ np.array(masterOrPhD)]
    
#     flnames= zip([stnm.split()[0] for stnm in studentInfo.STName.values],\
#                  [stnm.split()[-1] for stnm in studentInfo.STName.values])
#     isNameMatch = []
#     for stnm in majorStu.FullName:
#         isNameMatch.append(bool(sum([bool(findWholeWord(fn)(stnm)) &\
#                                      bool(findWholeWord(ln)(stnm)) for (fn,ln) in flnames])))
    
#     matchStu = majorStu[isNameMatch]
    linkin_st = zip(majorStu['File'].astype('int').values, majorStu['Index'].values)
    linkin_st = [(str(i),str(ln)) for (i,ln) in linkin_st]
#     stfn = [ for x in ]
#     matched_st = zip(matchStu['File'].astype('int').values, matchStu['Index'].values)
#     matched_st = [(str(i),str(ln)) for (i,ln) in matched_st]
    notmatched = [x for x in linkin_st if x not in matched_st]
    results[name] = [len(linkin_st),len(notmatched),len(linkin_st) - len(notmatched)]

# <codecell>

results

# <codecell>

results

# <codecell>

results

# <codecell>

results

# <codecell>

name = 'physics'
isMajorMatch = [(bool(findWholeWord(name)(major)) or bool(findWholeWord(name)(degree))) and \
                (not bool(findWholeWord('education')(major)))\
                for (major,degree) in zip(recordedStu['Major'].values,recordedStu['Degree'].values)]
majorStu = recordedStu[isMajorMatch]
degrees = [''.join(x.split('.')) for x in majorStu.Degree]
masterOrPhD = []
for stdg in degrees:
    mas = False
    for dg in mst:
        if(findWholeWord(dg)(stdg)):
            mas = True
    masterOrPhD.append(mas)
majorStu = majorStu[~ np.array(masterOrPhD)]
# flnames= zip([stnm.split()[0] for stnm in studentInfo.STName.values],\
#              [stnm.split()[-1] for stnm in studentInfo.STName.values])
# isNameMatch = []
# for stnm in majorStu.FullName:
#     isNameMatch.append(bool(sum([bool(findWholeWord(fn)(stnm)) &\
#                                  bool(findWholeWord(ln)(stnm)) for (fn,ln) in flnames])))
# matchStu = majorStu[isNameMatch]

linkin_st = zip(majorStu['File'].astype('int').values, majorStu['Index'].values)
linkin_st = [(str(i),str(ln)) for (i,ln) in linkin_st]
#     stfn = [ for x in ]
unmatchStu = majorStu[~np.array([(i,ln) in matched_st for (i,ln) in linkin_st])]
matched_st = zip(matchStu['File'].astype('int').values, matchStu['Index'].values)
matched_st = [(str(i),str(ln)) for (i,ln) in matched_st]
notmatched = [x for x in linkin_st if x not in matched_st]
results[name] = [len(linkin_st),len(notmatched),len(matched_st)]

# <codecell>

degree = [''.join(x.split('.')) for x in recordedStu.Degree]
major = [''.join(x.split('.')) for x in recordedStu.Major]

# <codecell>

a = pd.Series(degree).value_counts().index.tolist()
a.sort()
a

