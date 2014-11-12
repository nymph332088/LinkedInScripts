# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pylab as plt
import re
import string
import difflib
import Levenshtein
def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search
mst = ['masters','master','MA', 'MS', 'MEd', 'MSc', 'MEB', 'MDes', 'MNCM', 'MSN', \
       'MSW', 'MPA', 'MPC', 'MPP','MPH', 'MC', 'MCA', 'MCouns', 'MLA', 'MLIS', 'MDiv', \
       'ALM', 'MiM', 'MBA','emba','iMBA', 'MBA Tech', 'MCom', 'MBus', 'MI', 'PSM', \
       'MEng', 'MMath', 'MPhys', 'MPsych', 'MSci', 'MChem', 'MBiol', 'MGeol',\
       'dpm','dmd','doctor','phd','ph d','dphi','doctorate','post-doc']
# studentInfo = pd.read_csv('../studentInfo5.csv',sep='\t',dtype=object)
# print studentInfo.shape
# majorDict = pd.read_csv('../majordict.csv', sep='\t',dtype=object)
# majorDict.index = majorDict.ID

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
# mjnmLinkin= {}
# for key in mid_st_dict.keys():
#     # 5th column in file
#     mjnmLinkin[key] = []
#     for st in mid_st_dict[key]:
#         fn = int(float(st_mathced_Info.ix[st].MTResults.split(';')[0]))
#         ln = int(float(st_mathced_Info.ix[st].MTResults.split(';')[1]))
#         mjnmLinkin[key].append(open('part-%05d' %(fn),'rb').readlines()[ln].split('\t')[5])

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

# studentInfo = pd.read_csv('../studentInfo5.csv',sep='\t')
# print len(studentInfo)
education = [ pd.read_csv('../part-%05d-education.csv' %i, sep='\t') for i in range(0,10)]
education = [edu[~pd.isnull(edu.FullName)] for edu in education]
for i, edu in enumerate(education):
    edu['File'] = np.zeros((len(edu),)) + i
education = pd.concat(education,axis=0)
education.FullName = education.FullName.str.title()
education.FirstName = education.FirstName.str.title()
education.LastName = education.LastName.str.title()
print len(education.groupby(['File','Index']))
templeStu = education[[bool(findWholeWord('temple')(uni)) for uni in  education.University]]
print len(templeStu.groupby(['File','Index']))
recordedStu = templeStu[(templeStu.StartYear.astype('float')<=2010) & (templeStu.StartYear.astype('float')>=1997)]
print len(recordedStu)
print len(recordedStu.groupby(['File','Index']))
recordedStu.Major[pd.isnull(recordedStu.Major)] = ''
recordedStu.Degree[pd.isnull(recordedStu.Degree)]= ''
bachelorStu = recordedStu
degrees = [''.join(x.split('.')) for x in bachelorStu.Degree]
majors = [''.join(x.split('.')) for x in bachelorStu.Major]
masterOrPhD = []
for (stdg,stmj) in zip(degrees,majors):
    mas = False
    for dg in mst:
        if bool(findWholeWord(dg)(stdg)) | bool(findWholeWord(dg)(stmj)):
            mas = True
    masterOrPhD.append(mas)
bachelorStu = bachelorStu[~ np.array(masterOrPhD)]
print len(bachelorStu.groupby(['File','Index']))
# additional = [y for x in studentInfo.All_majors.astype('S') for y in x.split(';')] +\
#             [x for x in studentInfo.Entry_Major.astype('S')]
# additional = np.unique(np.array(additional))
# notin = [x for x in additional if x not in majorDict.index.values]
# majorDict.Name = [name.translate(string.maketrans("",""), string.punctuation) for name in majorDict.Name]
# studentInfo['EntryMjName'] = majorDict.ix[studentInfo.Entry_Major.astype('S').values[:]].Name.values
# studentInfo['EndMjName'] = majorDict.ix[studentInfo.EndMj.astype('S').values[:]].Name.values
# studentInfo['UniqMajorName'] = [';'.join(majorDict.ix[major.split(';')].Name.values) \
#                                 for major in studentInfo.Unique_Majors.astype('S').values]
# studentInfo['AllMajorName'] = [';'.join(majorDict.ix[major.split(';')].Name.values) \
#                                 for major in studentInfo.All_majors.astype('S').values]
# studentInfo['GradMjExName'] = [majorDict.ix[major] for major in studentInfo.GradMj_Extracted.astype('S').values]
# studentInfo['GradMjReName'] = [majorDict.ix[major] for major in studentInfo.GradMj_Reported.astype('S').values]

# <codecell>

len(bachelorStu)

# <codecell>

##################Join StudentInfo Table with Education table by LastName ###############
# Merge the education table.
studentInfo = pd.read_csv('../studentInfo5.csv',sep='\t',dtype='object')
education = [ pd.read_csv('../part-%05d-education.csv' %i, sep='\t') for i in range(0,10)]
print len(education)
education = [edu[~pd.isnull(edu.FullName)] for edu in education]
for i, edu in enumerate(education):
    edu['File'] = np.zeros((len(edu),)) + i
education = pd.concat(education,axis=0)
education.FullName = education.FullName.str.title()
education.FirstName = education.FirstName.str.title()
education.LastName = education.LastName.str.title()
print len(education.groupby(['File','Index']))

# Preprocessing the names of Education Table
education.FullName = [name.split(',')[0] for name in education.FullName] ## Remove the afflication in the names
education.FullName = [name.translate(string.maketrans("",""), string.punctuation) for name in education.FullName]
education.FirstName = [' '.join(name.split()[:-1]) for name in education.FullName]
education.LastName = [name.split()[-1] for name in education.FullName]

# Remove the records that has no temple university background
education.University[pd.isnull(education.University)] = ''
reg = re.compile(r'(?i)\b(?:%s)\b' % ('temple'), re.IGNORECASE)
education = education[[bool(reg.search(uni)) for uni in  education.University.values]]
print len(education)

# Remove whoever are master or doctorate
education.Degree[pd.isnull(education.Degree)] = ''
education.Major[pd.isnull(education.Major)] = ''
education.Major = [' '.join(major.translate(string.maketrans("",""),string.punctuation).split()) for major in education.Major]
education.Degree = [' '.join(degree.translate(string.maketrans("",""),string.punctuation).split()) for degree in education.Degree]
degrees = [''.join(x.split('.')) for x in education.Degree]
majors = [''.join(x.split('.')) for x in education.Major]
reg = re.compile(r'(?i)\b(?:%s)\b' % ('|'.join(mst)), re.IGNORECASE)
masterOrPhD = [bool(reg.search(stdg)) | bool(reg.search(stmj)) for (stdg,stmj) in zip(degrees,majors)]
education = education[~ np.array(masterOrPhD)]
education = education[~ ((education.StartYear.astype('float') < 1997) \
                         | (education.StartYear.astype('float') > 2011))]

# Join table with last name matching 
joinedTable = pd.merge(studentInfo, education, on='LastName',how='inner')
print len(joinedTable.groupby('Index_x'))
print len(joinedTable)

# Check the inexact match in the first name. Consider only the firstnames without the first character
# Exact Matched student
exactMatch = [bool(re.compile(r'(?i)\b(?:%s)\b' % (row['FirstName_x']), re.IGNORECASE).search(row['FirstName_y'])) \
              for index,row in joinedTable.iterrows()]
exactMatchTable = joinedTable[exactMatch]

# inexactMatchTable = joinejoinedTable
len(exactMatchTable.groupby('Index_x'))

# <codecell>

columnstowrite = ['STName','FullName','StartYear_x','StartYear_y',\
                  'EndYear_x','EndYear_y','UniqMajorName','Major','Degree','Index_x','Index_y',\
                  'File','Graduated_or_not','GradMjExName','GradMjReName']
joinedTable[columnstowrite].to_csv('all.csv',index=True)

# <codecell>

inexactMatchTable = joinedTable
# inexactMatchTable = inexactMatchTable[inexactMatchTable.FirstName_y != '']
matchRatio = 0.6
inexactMatch = [[Levenshtein.ratio(x[1:], row['FirstName_x'][1:]) for x in row['FirstName_y'].split() \
                 if (len(row['FirstName_y'])>1) & (x[0] == row['FirstName_x'][0])] \
                for index,row in inexactMatchTable.iterrows()]
inexactMatch = np.array([max(x) if x else 0 for x in inexactMatch]) >= matchRatio
inexactMatchTable = inexactMatchTable[inexactMatch]
print len(inexactMatchTable)
# # Inexact Match for the remaining students
# inexactMatchTable = joinedTable[~ np.array(exactMatch)]
# inexactMatchTable = inexactMatchTable[inexactMatchTable.FirstName_y != '']
# matchRatio = 0.7
# inexactMatch = [ (row['FirstName_x'][0] == row['FirstName_y'][0]) & \
#                 (Levenshtein.ratio(row['FirstName_x'][1:],row['FirstName_y'][1:])>= matchRatio) \
#                 for index,row in inexactMatchTable.iterrows()]
# inexactMatchTable = inexactMatchTable[inexactMatch]

# <codecell>

# Manual Match Results:
manual_match = pd.read_csv('../inexactmatch_manual_backup.csv',index_col=0)
manual_match.Match_or_Not[pd.isnull(manual_match.Match_or_Not)] = 0
manual_match.Match_or_Not = manual_match.Match_or_Not.astype('bool')
manual_match = manual_match.Match_or_Not
columnstowrite = ['STName','FullName','StartYear_x','StartYear_y',\
                  'EndYear_x','EndYear_y','UniqMajorName','Major','Degree','Index_x','Index_y',\
                  'File','Graduated_or_not','GradMjExName','GradMjReName']
manualMatchTable = inexactMatchTable.ix[manual_match.index[~manual_match]]
manualMatchTable.drop_duplicates(cols=['LastName','Index_x','Index_y','File'], take_last=True, inplace = True)
manualMatchTable[columnstowrite].to_csv('../inexactmatch_mamual_removedup.csv',index=True)
print len(manualMatchTable.groupby('Index_x'))
print pd.Series([len(gr) for key,gr in manualMatchTable.groupby(['Index_y','File'])]).value_counts()
print pd.Series([len(gr) for key,gr in manualMatchTable.groupby(['Index_x'])]).value_counts()
# exceptiongr = [gr for key, gr in manualMatchTable.groupby(['Index_x']) if len(gr) > 1]
# exceptiongr = [gr for key, gr in manualMatchTable.groupby(['Index_y','File']) if len(gr) > 1]
# exceptiongr = pd.concat(exceptiongr,axis=0)
# exceptiongr[columnstowrite].to_csv('../exception.csv',index=True)
exception_manual = pd.read_csv('../exception_manual.csv',index_col=0) ## Remove the multiple matching for our records
exception_manual = pd.read_csv('../exception_manual_2.csv',index_col=0) ## Remove the multiple matching for linkedin records
exception_manual.Remove_or_not[pd.isnull(exception_manual.Remove_or_not)] = 0
exception_manual = exception_manual.Remove_or_not.astype('bool')
manualMatchTable.drop(labels = exception_manual.index[exception_manual],inplace=True)
print len(manualMatchTable.groupby('Index_x'))

print pd.Series([len(gr) for key,gr in manualMatchTable.groupby(['Index_y','File'])]).value_counts()
print pd.Series([len(gr) for key,gr in manualMatchTable.groupby(['Index_x'])]).value_counts()
# Analyze the Matching bias
# Year bias
manualMatchTable[columnstowrite].to_csv('../manualMatchedTable_short.csv',index=True)
print float(sum(manualMatchTable.Graduated_or_not.astype('int').astype('bool')))/sum(studentInfo.Graduated_or_not.astype('int').astype('bool'))
print sum(~studentInfo.Graduated_or_not.astype('int').astype('bool'))

# <codecell>

names = ['physics','math','mathematics','chemistry']
st_mathced_Info = studentInfo[studentInfo.NumMT != 0]
matched_st = [tuple(x.split(';')[:2]) for x in st_mathced_Info.MTResults]
recordedStu.Major[pd.isnull(recordedStu.Major)] = ''
recordedStu.Degree[pd.isnull(recordedStu.Degree)]= ''
results = {}
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
degree = [''.join(x.split('.')) for x in recordedStu.Degree]
major = [''.join(x.split('.')) for x in recordedStu.Major]

