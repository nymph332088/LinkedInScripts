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
# def findWholeWord(w):
#     return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search
# mid_st_dict = {}
# for id in missingIds:
#     mid_st_dict[id] = [sind for sind in st_mathced_Info.index if id in st_mathced_Info.ix[sind].All_majors.split(';')]
mst = ['masters','master','MA', 'MS', 'MEd', 'MSc', 'MEB', 'MDes', 'MNCM', 'MSN', \
       'MSW', 'MPA', 'MPC', 'MPP','MPH', 'MC', 'MCA', 'MCouns', 'MLA', 'MLIS', 'MDiv', \
       'ALM', 'MiM', 'MBA','emba','iMBA', 'MBA Tech', 'MCom', 'MBus', 'MI', 'PSM', \
       'MEng', 'MMath', 'MPhys', 'MPsych', 'MSci', 'MChem', 'MBiol', 'MGeol',\
       'dpm','dmd','doctor','phd','ph d','dphi','doctorate','post-doc']
ID = {'6030500':'Advertising Graphic Design','8020310':'Elementary Education','19140000':'Geology',\
      '21030020':'Tourism','3050001':'Africa America Study','5132100':'International Business','5131500':'Business',
      '5131700':'Business Law','6020000':'Journalism','12680010':'HealthInfo Management','17010000':'Math',\
      '5000105':'Business Management','22010100':'Women Study','21030030':'Sports RecreationManage','5000104':'Business Management',\
      '19808000':'Environmental Study','6060000':'Mass Media','5131300':'Finance','22040300':'Economics',\
      '15090000':'Philosophy','8030700':'Secondary Education','54020500':'Community Reginal Relation',\
      '7010100':'Magage Info System','7020000':'Computer Science','7020100':'Info Science and Tech',\
      '12030000':'Registed Nurse','22140350':'Cartography','6090000':'Communication General',\
      '6080000':'Speech Communication','5110000':'Real Estate','9220100':'Environmental Engineering',\
      '5000100':'Business Administration'}
studentInfo = pd.read_csv('../studentInfo5.csv',sep='\t',dtype=object)
print studentInfo.shape
majorDict = pd.read_csv('../majordict.csv', sep=',',dtype='object')
majorDict.Name[pd.isnull(majorDict.Name)] = ''
majorDict.Name = [name.translate(string.maketrans("",""), string.punctuation) for name in majorDict.Name]
majorDict.loc[len(majorDict)] = ['','']
majorDict.index = majorDict.ID
%pylab inline
manualMatchTable = pd.read_csv('../manualMatchedTable.csv',index_col=0,dtype=object)
studentNonGrad = studentInfo[~studentInfo.Graduated_or_not.astype('int').astype('bool')]
studentGrad = studentInfo[studentInfo.Graduated_or_not.astype('int').astype('bool')]
studentGrad.GradMj_Reported[pd.isnull(studentGrad.GradMj_Reported)] = ''
studentGrad.GradMjReName = [majorDict.ix[major].Name for major in studentGrad.GradMj_Reported.astype('object')]
manualGrad = manualMatchTable[manualMatchTable.Graduated_or_not.astype('int').astype('bool')]
manualGrad.GradMjReName = studentGrad.ix[manualGrad.Index_x.astype('int')].GradMjReName.values
# studentInfo['EntryMjName'] = majorDict.ix[studentInfo.Entry_Major.astype('S').values[:]].Name.values
# studentInfo['EndMjName'] = majorDict.ix[studentInfo.EndMj.astype('S').values[:]].Name.values
# studentInfo.Unique_Majors[pd.isnull(studentInfo.Unique_Majors)] = ''
# studentInfo.All_majors[pd.isnull(studentInfo.All_majors)] = ''
# studentInfo.GradMj_Extracted[pd.isnull(studentInfo.GradMj_Extracted)] = ''
# studentInfo.GradMj_Reported[pd.isnull(studentInfo.GradMj_Reported)] = ''
# studentInfo['UniqMajorName'] = [';'.join(majorDict.ix[major.split(';')].Name.values) \
#                                 for major in studentInfo.Unique_Majors.astype('S').values]
# studentInfo['AllMajorName'] = [';'.join(majorDict.ix[major.split(';')].Name.values) \
#                                 for major in studentInfo.All_majors.astype('S').values]
# studentInfo['GradMjExName'] = [majorDict.ix[major] for major in studentInfo.GradMj_Extracted.astype('S').values]
# studentInfo['GradMjReName'] = [majorDict.ix[major] for major in studentInfo.GradMj_Reported.astype('S').values]

# <codecell>

################## Check the missing rate for linkedin data in our records ###############
# Merge the education table.
education = [ pd.read_csv('../part-%05d-education.csv' %i, sep='\t') for i in range(0,10)]
education = [edu[~pd.isnull(edu.FullName)] for edu in education]
for i, edu in enumerate(education):
    edu['File'] = np.zeros((len(edu),)) + i
education = pd.concat(education,axis=0)
education.FullName = education.FullName.str.title()
education.FirstName = education.FirstName.str.title()
education.LastName = education.LastName.str.title()
print len(education)
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

# Keep only students from 1997 - 2011
education = education[((education.StartYear.astype('float') >= 1997) \
                         & (education.StartYear.astype('float') <= 2011))]
print len(education)
# Remove whoever are master or doctorate
education.Degree[pd.isnull(education.Degree)] = ''
education.Major[pd.isnull(education.Major)] = ''
education.Major = [' '.join(major.translate(string.maketrans("",""),string.punctuation).split()) for major in education.Major]
education.Degree = [' '.join(degree.translate(string.maketrans("",""),string.punctuation).split()) for degree in education.Degree]
education.Major = education.Major.str.title()
education.Degree = education.Degree.str.title()
degrees = [''.join(x.split('.')) for x in education.Degree]
majors = [''.join(x.split('.')) for x in education.Major]
reg = re.compile(r'(?i)\b(?:%s)\b' % ('|'.join(mst)))
masterOrPhD = [bool(reg.search(stdg)) | bool(reg.search(stmj)) for (stdg,stmj) in zip(degrees,majors)]
education = education[~ np.array(masterOrPhD)]
print len(education)

# <codecell>

keywords = ['chemistry']
keywordsnot = ['education','teaching']
mgm = [bool(re.compile(r'(?i)\b(?:%s)\b' % ('|'.join(keywords))).search(major)) & \
       (not bool(re.compile(r'(?i)\b(?:%s)\b' % ('|'.join(keywordsnot))).search(major)))\
                      for major in uniqueMajorsLinkedIn.index]
print uniqueMajorsLinkedIn[mgm]
sum(uniqueMajorsLinkedIn[mgm])

# <codecell>

##### IST records in LinkedIn but Not in Our Data
keywords = ['computer','information','info','tech','ist','is']
keywordsnot = ['management','health','education']
mgm = [bool(re.compile(r'(?i)\b(?:%s)\b' % ('|'.join(keywords))).search(major)) & \
       (not bool(re.compile(r'(?i)\b(?:%s)\b' % ('|'.join(keywordsnot))).search(major)))\
                      for major in education.Major]

print sum(mgm)
columnstowrite = ['FullName','StartYear','EndYear','Major','Degree']
# education[mgm][columnstowrite].to_csv('../IST_manual.csv',index=True)
IST_manual = pd.read_csv('../IST_manual.csv',index_col=0)
IST_manual.Match_or_Not[pd.isnull(IST_manual.Match_or_Not)] = 0
IST_manual = education[mgm][IST_manual.Match_or_Not.astype('bool')]
IST_manual.drop_duplicates(cols=['Index','File'],inplace = True, take_last=True)
matched_st = zip(manualMatchTable.Index_y.astype('int'), manualMatchTable.File.astype('float'))
IST_st = zip(IST_manual.Index, IST_manual.File)
print len(IST_manual)
sum([st not in matched_st for st in IST_st])

# <codecell>

##### Physics records in LinkedIn but Not in Our Data
keywords = ['physics']
mgm = [bool(re.compile(r'(?i)\b(?:%s)\b' % ('|'.join(keywords))).search(major))\
                      for major in education.Major]

print sum(mgm)
columnstowrite = ['FullName','StartYear','EndYear','Major','Degree']
# education[mgm][columnstowrite].to_csv('../pysics_manual.csv',index=True)
IST_manual = pd.read_csv('../pysics_manual.csv',index_col=0)
IST_manual.Match_or_Not[pd.isnull(IST_manual.Match_or_Not)] = 0
IST_manual = education[mgm][IST_manual.Match_or_Not.astype('bool')]
IST_manual.drop_duplicates(cols=['Index','File'],inplace = True, take_last=True)
matched_st = zip(manualMatchTable.Index_y.astype('int'), manualMatchTable.File.astype('float'))
IST_st = zip(IST_manual.Index, IST_manual.File)
print len(IST_manual)
sum([st not in matched_st for st in IST_st])

# <codecell>

keywords = ['math','mathmatics','mathematics','mathematic']
keywordsnot = ['education','teaching']
mgm = [bool(re.compile(r'(?i)\b(?:%s)\b' % ('|'.join(keywords))).search(major)) & \
       (not bool(re.compile(r'(?i)\b(?:%s)\b' % ('|'.join(keywordsnot))).search(major)))\
                      for major in education.Major]

print sum(mgm)
columnstowrite = ['FullName','StartYear','EndYear','Major','Degree']
# education[mgm][columnstowrite].to_csv('../math_manual.csv',index=True)
IST_manual = pd.read_csv('../math_manual.csv',index_col=0)
IST_manual.Match_or_Not[pd.isnull(IST_manual.Match_or_Not)] = 0
IST_manual = education[mgm][IST_manual.Match_or_Not.astype('bool')]
IST_manual.drop_duplicates(cols=['Index','File'],inplace = True, take_last=True)
matched_st = zip(manualMatchTable.Index_y.astype('int'), manualMatchTable.File.astype('float'))
IST_st = zip(IST_manual.Index, IST_manual.File)
print len(IST_manual)
sum([st not in matched_st for st in IST_st])

# <codecell>

keywords = ['chem','chemistry']
keywordsnot = ['education','teaching']
# mgm = [bool(re.compile(r'(?i)\b(?:%s)\b' % ('|'.join(keywords))).search(major)) & \
#        (not bool(re.compile(r'(?i)\b(?:%s)\b' % ('|'.join(keywordsnot))).search(major)))\
#                       for major in education.Major]

mgm = [bool(major.lower() == 'chemistry') for major in education.Major]
print sum(mgm)
columnstowrite = ['FullName','StartYear','EndYear','Major','Degree']
# education[mgm][columnstowrite].to_csv('../chem_manual.csv',index=True)
IST_manual = pd.read_csv('../chem_manual.csv',index_col=0)
IST_manual.Match_or_Not[pd.isnull(IST_manual.Match_or_Not)] = 0
IST_manual = education[mgm][IST_manual.Match_or_Not.astype('bool')]
IST_manual.drop_duplicates(cols=['Index','File'],inplace = True, take_last=True)
matched_st = zip(manualMatchTable.Index_y.astype('int'), manualMatchTable.File.astype('float'))
IST_st = zip(IST_manual.Index, IST_manual.File)
print len(IST_manual)
sum([st not in matched_st for st in IST_st])

# <codecell>

IST_manual[columnstowrite+['LastName','Index','File'，]][[st not in matched_st for st in IST_st]]

# <codecell>

%pylab inline
# manualMatchTable = pd.read_csv('../manualMatchedTable.csv',index_col=0,dtype='object')
x = manualMatchTable.EndYear_x[manualMatchTable.Graduated_or_not.astype('int').astype('bool')]
y = studentInfo.EndYear[studentInfo.Graduated_or_not.astype('int').astype('bool')]
totalCounts = np.log2(x.value_counts()+1)
counts = np.log2(y.value_counts()+1)
k = len(counts)
fig, ax = plt.subplots()
width = 0.35
ind = np.arange(k)
rect1 = ax.bar(ind, counts.iloc[:k],width, color='r')
rect2 = ax.bar(ind+width, totalCounts.ix[counts.iloc[:k].index],width, color='b')
labels = counts.iloc[:k].index
# labels[pd.isnull(labels)] = labels[pd.isnull(labels)].index
plt.xticks(ind+2*width, labels, rotation = 45, ha='right')
for i in ind:
    plt.text(i+width, counts.values[i], \
             '%.2f'%(np.divide(totalCounts.ix[counts.iloc[:k].index], counts).values[i]),\
             ha='center')

plt.title('Sampling Bias of the Graduation Year for Graduated Students')
ax.set_ylabel('Log2 Number of students')
ax.set_xlabel('Graduation Year')
plt.legend((rect1[0],rect2[0]),('Grad_all','Grad_matched'))

# plt.title('Bias of the Last Recorded Year for nonGraduated Students')
# ax.set_ylabel('Log2 Number of students')
# ax.set_xlabel('Last Recorded Year')
# plt.legend((rect1[0],rect2[0]),('NonGrad_all','NonGrad_matched'))

plt.gcf().tight_layout()
plt.subplots_adjust(top=0.9) 

# <codecell>

%pylab inline
width = 0.35
totalCounts = studentGrad.GradMjReName
totalCounts = np.log2(totalCounts.value_counts()+1)
counts = manualGrad.GradMjReName
counts = np.log2(counts.value_counts()+1)
k = np.linspace(0, 34, num=35)
# k = np.linspace(31, 60, num = 30)
fig, ax = plt.subplots()
ind = k
rect1 = ax.bar(ind, totalCounts.iloc[k], width, color='r')
rect2 = ax.bar(ind+width, counts.ix[totalCounts.iloc[k].index],width, color='b')
labels = totalCounts.iloc[k].index
plt.xticks(ind+2*width, labels, rotation = 45, ha='right')
for i in ind:
    plt.text(i+width, totalCounts.values[i], \
             '%.2f'%(np.divide(counts.ix[totalCounts.index], totalCounts).values[i]),\
             ha='center')

plt.title('Bias of Majors for Graduated Students')
ax.set_ylabel('Log2 Number of students')
ax.set_xlabel('Major')
plt.legend((rect1[0],rect2[0]),('Grad_all','Grad_matched'))

plt.gcf().tight_layout()
plt.subplots_adjust(top=0.9)
fig.set_size_inches(20,20.5)
# plt.savefig('pic/entrymajor_vs_endmajor.png')
# plt.set_xticks(ind + 0.5/2)
# ax.set_xticklabels(EndMj.iloc[:10].index)

# <codecell>

years = [str(y) for y in range(1998,2011)]
majors = totalCounts.iloc[:34].index
tnum = pd.DataFrame(columns=majors, index=years)
mnum = pd.DataFrame(columns=majors, index=years)
data = {key:gr.EndYear.value_counts() for key,gr in studentGrad.groupby(['GradMjReName'])}
data2 = {key:gr.EndYear_x.value_counts() for key,gr in manualGrad.groupby(['GradMjReName'])}
for major in majors:
    if major in data.keys(): tnum[major].ix[data[major].index] = data[major].values
    if major in data2.keys(): mnum[major].ix[data2[major].index] = data2[major].values
tnum[pd.isnull(tnum)] = 0
mnum[pd.isnull(mnum)] = 0

# <codecell>

%pylab inline
# manualMatchTable = pd.read_csv('../manualMatchedTable.csv',index_col=0,dtype='object')
major = majors[0]
for index,major in enumerate(majors[:20]):
    totalCounts = np.log2(tnum[major].astype('float')+1)
    counts = np.log2(mnum[major].astype('float')+1)
    k = len(counts)
    fig, ax = plt.subplots()
    width = 0.35
    ind = np.arange(k)
    rect1 = ax.bar(ind, totalCounts,width, color='r')
    rect2 = ax.bar(ind+width, counts,width, color='b')
    labels = totalCounts.index
    # labels[pd.isnull(labels)] = labels[pd.isnull(labels)].index
    plt.xticks(ind+2*width, labels, rotation = 45, ha='right')
    for i in ind:
        plt.text(i+width, totalCounts.values[i], \
                 '%.2f'%(np.divide(counts, totalCounts).values[i]),\
                 ha='center')

    plt.title('%s Sampling Bias in each year' % major)
    ax.set_ylabel('Log2 Number of students')
    ax.set_xlabel('Graduation Year')
    plt.legend((rect1[0],rect2[0]),('Grad_all','Grad_matched'),loc='best')

    # plt.title('Bias of the Last Recorded Year for nonGraduated Students')
    # ax.set_ylabel('Log2 Number of students')
    # ax.set_xlabel('Last Recorded Year')
    # plt.legend((rect1[0],rect2[0]),('NonGrad_all','NonGrad_matched'))

    plt.gcf().tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.savefig('../pic/%d %s bias in each year.png' % (index, major))

