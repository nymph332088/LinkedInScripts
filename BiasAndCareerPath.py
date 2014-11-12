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
columnstowrite = ['STName','FullName','StartYear_x','StartYear_y',\
                  'EndYear_x','EndYear_y','UniqMajorName','Major','Degree','Index_x','Index_y',\
                  'File','Graduated_or_not','GradMjExName','GradMjReName']
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
majors = ['BIOLOGY', 'BIOCHEMISTRY', 'CHEMISTRY', 'Computer Science',  'Info Science and Tech']
studentInfo = pd.read_csv('../studentInfo5.csv',sep='\t',dtype=object)
print studentInfo.shape
majorDict = pd.read_csv('../majordict.csv', sep=',',dtype='object')
majorDict.Name[pd.isnull(majorDict.Name)] = ''
majorDict.Name = [name.translate(string.maketrans("",""), string.punctuation) for name in majorDict.Name]
majorDict.loc[len(majorDict)] = ['','']
majorDict.index = majorDict.ID
%pylab inline
manualMatchTable = pd.read_csv('../manualMatchedTable_backup.csv',sep='\t',index_col=0,dtype=object)
studentNonGrad = studentInfo[~studentInfo.Graduated_or_not.astype('int').astype('bool')]
studentGrad = studentInfo[studentInfo.Graduated_or_not.astype('int').astype('bool')]
manualGrad = manualMatchTable[manualMatchTable.Graduated_or_not.astype('int').astype('bool')]

# manualMatchTable.UniqMajorName = studentInfo.ix[manualMatchTable.Index_x.astype('int')].UniqMajorName.values
# manualMatchTable.GradMjExName =  studentInfo.ix[manualMatchTable.Index_x.astype('int')].GradMjExName.values
# manualMatchTable.GradMjReName =  studentInfo.ix[manualMatchTable.Index_x.astype('int')].GradMjReName.values
# manualMatchTable.AllMajorName =  studentInfo.ix[manualMatchTable.Index_x.astype('int')].AllMajorName.values
# manualMatchTable.EndMjName =  studentInfo.ix[manualMatchTable.Index_x.astype('int')].EndMjName.values
# manualMatchTable.EntryMjName =  studentInfo.ix[manualMatchTable.Index_x.astype('int')].EntryMjName.values

# <codecell>

manualGrad = manualGrad[manualGrad.SAT.astype('float') !=0]
studentGrad = studentGrad[studentGrad.SAT.astype('float') != 0]
# manualGrad.GradMjReName[manualGrad.GradMjReName == 'COMPUTER SCIENCE 08'] = 'Computer Science'
# studentGrad.GradMjReName[studentGrad.GradMjReName == 'COMPUTER SCIENCE 08'] = 'Computer Science'
# studentGrad.GradMjReName[studentGrad.GradMjReName == 'INFO SCIENCE  TECH 08'] = 'Info Science and Tech'
# manualGrad.GradMjReName[manualGrad.GradMjReName == 'INFO SCIENCE  TECH 08'] = 'Info Science and Tech'
matchGrad = studentGrad[studentGrad.Index.isin(manualGrad.Index_x)]
nonmatchGrad = studentGrad[~studentGrad.Index.isin(manualGrad.Index_x)]
years = [str(y) for y in range(1998,2011)]
mnum = pd.DataFrame(columns=majors, index=years)
nmnum = pd.DataFrame(columns=majors, index=years)
data = {key:gr.EndYear.value_counts() for key,gr in matchGrad.groupby(['GradMjReName'])}
data2 = {key:gr.EndYear.value_counts() for key,gr in nonmatchGrad.groupby(['GradMjReName'])}
for major in majors:
    if major in data.keys(): mnum[major].ix[data[major].index] = data[major].values
    if major in data2.keys(): nmnum[major].ix[data2[major].index] = data2[major].values
mnum[pd.isnull(mnum)] = 0
nmnum[pd.isnull(nmnum)] = 0
from scipy.stats import ttest_ind
reps = {}
for major in majors: reps[major] = 0
siglevel = 0.05
for rep in range(1):
    results = {}
    results['Major'] = []
    results['CountsM'] = []
    results['CountsNonM'] = []
    results['MatchMean'] = []
    results['NonMatchMean'] = []
    results['TStatistic'] = []
    results['Pvalue'] = []
    for major in majors:
#         minbyyear = pd.DataFrame([mnum[major],nmnum[major]]).min(axis=0)
        minbyyear = mnum[major]
        results['CountsM'].append(sum(minbyyear))

        msample = []

        [msample.extend(np.random.choice(matchGrad[(matchGrad.EndYear == year) & \
                                                   (matchGrad.GradMjReName == major)].Index.astype('int'),\
                                         minbyyear.ix[year],replace=False).tolist())\
         for year in years if minbyyear.ix[year] != 0]

        minbyyear = nmnum[major]
        results['CountsNonM'].append(sum(minbyyear))
        nmsample = []

        [nmsample.extend(np.random.choice(nonmatchGrad[(nonmatchGrad.EndYear == year) & \
                                                       (nonmatchGrad.GradMjReName==major)].Index.astype('int'),\
                                          minbyyear.ix[year],replace=False).tolist()) \
         for year in years if minbyyear.ix[year] != 0]
        results['Major'].append(major)

        mscore = matchGrad.ix[msample].GPA.astype('float')
        nmscore = nonmatchGrad.ix[nmsample].GPA.astype('float')
        results['MatchMean'].append('%6.3f' % mscore.mean())
        results['NonMatchMean'].append('%6.3f' % nmscore.mean())
        t, p =  ttest_ind(mscore.values, nmscore.values, equal_var=True)
        results['TStatistic'].append('%6.3f' % t)
        results['Pvalue'].append('%6.4f' % p)
        if p<= siglevel: reps[major] += 1 
results = pd.DataFrame(results)
results

# <codecell>

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

# <codecell>

k = 500
mjsts = pd.DataFrame()
recordcolnms = ['STName','Gender','GPA','SAT','Math_SAT','Verbal_SAT','GradMjReName']
jobs = []
edus = []
for major in majors:
    temp = manualGrad[manualGrad.GradMjReName == major]
    samplek = np.random.choice(temp.Index_x.values,np.min([k,len(temp)]), replace=False)
    temp = manualGrad[manualGrad.Index_x.isin(samplek)]
    for index, st in temp.iterrows():
        career = pd.read_csv('../part-%05d-experience.csv' %int(float(st['File'])), sep='\t')
        career = career[career.Index == int(st['Index_y'])]
        career.sort(columns=['StartYear'],inplace=True)
        edu = education[(education.File == int(float(st['File']))) & (education.Index == int(st['Index_y']))]
        edu.sort('StartYear',inplace=True)
        edustr = [':'.join(row[['University', 'Major', 'Degree', 'StartYear','EndYear']].astype('S'))\
                  for index,row in edu.iterrows()]
        record = pd.DataFrame(np.random.randn(1,len(recordcolnms)), columns=recordcolnms)
        for col in recordcolnms: record[col] = st[col]
        record['Duration'] = '-'.join(st[['StartYear_x','EndYear_x']].astype('i4').astype('S'))
        record['Education'] = ';'.join(edustr)
#         for i in range(len(edustr)):
#             record['edu_%d' %i] = edustr[i]
        for i in range(len(career)):
            record['comp_%d' %i] = career.iloc[i,:].Company 
            record['title_%d' %i] = career.iloc[i,:].Position
            record['year_%d' %i] = '-'.join(career.iloc[i,[3,5]].astype('S'))
        print len(career)
        jobs.append(len(career))
        edus.append(len(edustr))
        mjsts = mjsts.append(record)

# <codecell>

recordcolnms = ['STName','Gender','GPA','SAT','Math_SAT','Verbal_SAT','GradMjReName','Duration','Education']
[recordcolnms.extend(['comp_%d' %i,'title_%d' %i,'year_%d' %i]) for i in range(6)]
mjsts[recordcolnms].to_csv('../first6jobs2.csv',index=False,sep='\t')

# <codecell>

width = 0.35
for index,major in enumerate(majors):
    totalCounts = np.log2(nmnum[major].astype('float')+1)
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
                 '%.0f'%(pd.DataFrame([mnum[major],nmnum[major]]).min(axis=0).values[i]),\
                 ha='center')

    plt.title('%s graduated in LinkedIn vs not-in LinkedIn ' % major)
    ax.set_ylabel('Log2 Number of students')
    ax.set_xlabel('Graduation Year')
    plt.legend((rect1[0],rect2[0]),('In LinkedIn','Not-in LinkedIn'),loc='best')

    # plt.title('Bias of the Last Recorded Year for nonGraduated Students')
    # ax.set_ylabel('Log2 Number of students')
    # ax.set_xlabel('Last Recorded Year')
    # plt.legend((rect1[0],rect2[0]),('NonGrad_all','NonGrad_matched'))

    plt.gcf().tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.savefig('../pic/%d %s in vs not in.png' % (index, major))

