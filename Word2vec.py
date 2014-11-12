# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from libraries import *
import subprocess
import threading
import os
import time
import codecs
import errno
from gensim import models,similarities,corpora
# import sys
%pylab inline
import scipy.spatial.distance as distance
import scipy.cluster.hierarchy as sch

# <codecell>

def most_similar(model,term,prefix,n):
    try:
        topneigh = model.most_similar(term,topn=5*n)
        matchPref = [bool(x.startswith(prefix)) for x,sim in topneigh]
        topneigh = [topneigh[i] for i, elem in enumerate(matchPref) if elem]
    except KeyError:
        topneigh = []
    return topneigh
def procColumn(data, col,prefix):
    coldata = data[col].str.lower()
    coldata = [str(x).translate(string.maketrans(string.punctuation," "*len(string.punctuation)))\
            for x in coldata]
    coldata = ['_'.join(str(x).split()) for x in coldata]
    coldata = [prefix + x for x in coldata]
    return coldata

# <codecell>

model = models.Word2Vec.load_word2vec_format('../model_linkedin.bin', binary=True)
## 
samplest = pd.read_csv('../first6jobs2.csv',sep='\t')
voc = pd.read_csv('../vocab_linkedin.txt',header=None,sep=' ',names=['vocname','cluster'])
manualMatchTable = pd.read_csv('../manualMatchedTable_backup.csv',sep='\t',index_col=0)
majors = ['BIOLOGY', 'BIOCHEMISTRY', 'CHEMISTRY', 'Computer Science',  'Info Science and Tech']
manualMatchTable = pd.concat([manualMatchTable[manualMatchTable.GradMjReName == major] for major in majors],axis=0)
positionvoc = voc.vocname[voc.vocname.str.startswith('p_')]

# <codecell>

columns= []
[columns.extend(['title_%d' %i, 'tneigh_%d' %i,'comp_%d' %i,'cneigh_%d' %i]) for i in range(6)]
voc_check = pd.DataFrame(np.zeros((len(manualMatchTable),len(columns))), columns=columns) 
for i in range(6):
    col = 'title_%d'%i
    prefix = 'p_'
    n = 20
    coldata = procColumn(samplest, col, prefix)
    topks = [most_similar(model, term, prefix, n) for term in coldata]
    topks = [topk[:n] if(len(topk)) else [] for topk in topks]
    topks = ['%s' %([(str(a),'%.3f' %b) for a,b in topk]) if(len(topk)) else 'False' for topk in topks]
    voc_check[col] = coldata
    voc_check['tneigh_%d' %i] = topks
    
    print i 
    col = 'comp_%d' %i
    prefix = 'c_'
    n = 20
    coldata = procColumn(samplest, col, prefix)
    topks = [most_similar(model, term, prefix, n) for term in coldata]
    topks = [topk[:n] if(len(topk)) else [] for topk in topks]
    topks = ['%s' %([(str(a),'%.3f' %b) for a,b in topk]) if(len(topk)) else 'False' for topk in topks]
    voc_check[col] = coldata
    voc_check['cneigh_%d' %i] = topks
    print i 

for i in range(6):
    voc_check['cneigh_%d' %i][voc_check['comp_%d' %i]=='c_nan'] = 'False'
voc_check.to_csv('../jobs_companies_word2vec.csv',index=False)

# <codecell>

i = 0
col = 'title_%d' %i
prefix = 'p_'

col = 'comp_%d' %i
prefix = 'c_'

coldata = procColumn(samplest, col, prefix)
coldata = np.array(coldata)
coldata[coldata== prefix+'nan'] = 'nan'
word2vec = np.zeros((len(coldata), 300))
for index,job in enumerate(coldata):
    try:
        word2vec[index,:] = model[job]
    except KeyError:
        pass

print sum(sum(word2vec,1) !=0)
print 346 - sum(sum(word2vec,1) !=0)
pairwise_dists = distance.squareform(distance.pdist(word2vec,'euclidean'))
clusters = sch.linkage(pairwise_dists,method='complete')
row_den = sch.dendrogram(clusters,color_threshold=np.inf,no_plot=True)
pairwise_dists = distance.squareform(distance.pdist(word2vec.T,'euclidean'))
clusters = sch.linkage(pairwise_dists,method='complete')
col_den = sch.dendrogram(clusters,color_threshold=np.inf,no_plot=True)

# <codecell>

fig,ax = subplots(figsize=(10,10))
heatmap2 = ax.pcolor(word2vec[np.ix_(row_den['leaves'],\
                                      col_den['leaves'])],cmap=plt.cm.coolwarm)
ax.invert_yaxis()
ax.set_xlabel('Word2vec Representation')
ax.set_ylabel('%s of 346 students'%col)
plt.gcf().tight_layout()
fig.savefig('../pic/sorted_heatmap_%s.png' %col)

# <codecell>

ran = range(300,310)
fig,ax = subplots(figsize=(15,10))
heatmap2 = ax.pcolor(word2vec[np.ix_(np.array(row_den['leaves'])[ran],\
                                      col_den['leaves'])],cmap=plt.cm.coolwarm)
ax.invert_yaxis()
ax2 = ax.twinx()
ax2.invert_yaxis()
ax2.pcolor(word2vec[np.ix_(np.array(row_den['leaves'])[ran],\
                                      col_den['leaves'])],cmap=plt.cm.coolwarm)

ax.set_yticks(np.arange(10)+0.5)
ax.set_yticklabels(coldata[np.array(row_den['leaves'])[ran]])
for tick in ax.yaxis.get_major_ticks(): tick.label.set_fontsize(20)
ax2.set_yticks(np.arange(10) + 0.5)
ax2.set_yticklabels(manualMatchTable.GradMjReName.iloc[np.array(row_den['leaves'])[ran]].values, )
for tick in ax2.yaxis.get_major_ticks(): tick.label.set_fontsize(20)
ax.set_xlabel('Word2vec Representation')
ax.set_ylabel('%s of some students' %col)
plt.gcf().tight_layout()
fig.savefig('../pic/sorted_heatmap_%s_1.png' %col)

# <codecell>

pd.DataFrame(word2vec, columns = np.arange(300),index=coldata[np.array(row_den['leaves'])]).to_csv('../data.txt',sep=' ')

# <codecell>

comparison = pd.DataFrame(np.random.randn(len(manualMatchTable),6),\
                          columns=['Name','PositionNames_new','PositionNames_old','String_Old','File','Index'])
comparison.Name = manualMatchTable.STName.values
comparison.PositionNames_new = positnames_new
comparison.PositionNames_old = positionnames
comparison.String_Old = ststr
comparison.File = manualMatchTable.File.astype('i4').values
comparison.Index = manualMatchTable.Index_y.astype('i4').values

# <codecell>

word2vec = np.zeros((len(firstjob), 300))
for index,job in enumerate(firstjob):
    cmd = 'grep -w %s ../model_linkedin.txt' % job
    print cmd
    grebx = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    file_data = grebx.stdout.read()
    if file_data != '':
        word2vec[index,:] = map(float, file_data.split()[1:-1])
import csv
np.savetxt("../word2vecrepr.csv", word2vec, delimiter=",")

# <codecell>

fns = [int(float(row['File'])) for index, row in manualMatchTable.iterrows()]
lns = [int(row['Index_y']) for index,row in manualMatchTable.iterrows()]
ststr = [open('../part-%05d' %fn,'rb').readlines()[ln] for (fn,ln) in zip(fns,lns)]
positionnames = [line.split('\t')[8] for line in ststr]
posicols = []
[posicols.extend(['title_%d' %i]) for i in range(6)]
positnames_new = [' '.join(row[posicols].dropna().str.lower().str.split().str.join('_').astype('S').values) \
                  for index,row in samplest.iterrows()] 

