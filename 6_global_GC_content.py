'''
The script estimates GC content in CDS files 

by Ivan Pchelin, arcella.oraia@gmail.com
2022-02-11

#####################################################################
Visualization of GC_content_values_all_seqs.txt in R:

setwd("C:/Pchelin")
qwe <- read.table(file='GC_content_values_all_seqs.txt')
qweq <- as.matrix(qwe)
hist(qweq, breaks = 60, xlab = "GC content per CDS", ylab = "Number",
 main = NULL, las= 1)

#####################################################################
Visualization of GC_content_values_by_files.txt in R:

setwd("C:/Pchelin")
library(data.table)
library(psych)
qwe <- fread(file='GC_content_values_by_files.txt')[-1]
qwe <-as.data.frame(qwe, headers = TRUE)
multi.hist(qwe)


setwd("C:/Pchelin")
library(data.table)
library(tidyverse)
library(grid)
qwe <- fread(file='GC_content_values_by_files.txt')[-1]
qwe <-as_tibble(qwe, headers = TRUE)
qwe <- qwe%>%
 select(1:12)

hist(qwe[[1]], las=1, main = "113", xlab=NULL, ylab=NULL,breaks = 30,xlim=c(0.25,0.46))
hist(qwe[[2]], las=1, main = "EFDG1", xlab=NULL, ylab=NULL,breaks = 30,xlim=c(0.25,0.46))
hist(qwe[[3]], las=1, main = "EFGrKN", xlab=NULL, ylab=NULL,breaks = 30,xlim=c(0.25,0.46))
hist(qwe[[4]], las=1, main = "EFGrNG", xlab=NULL, ylab=NULL,breaks = 30,xlim=c(0.25,0.46))
hist(qwe[[5]], las=1, main = "EFP01", xlab=NULL, ylab=NULL,breaks = 30,xlim=c(0.25,0.46))
hist(qwe[[6]], las=1, main = "EfV12", xlab=NULL, ylab=NULL,breaks = 30,xlim=c(0.25,0.46))
hist(qwe[[7]], las=1, main = "GVEsP-1", xlab=NULL, ylab=NULL,breaks = 30,xlim=c(0.25,0.46))
hist(qwe[[8]], las=1, main = "iF6", xlab=NULL, ylab=NULL,breaks = 30,xlim=c(0.25,0.46))
hist(qwe[[9]], las=1, main = "PEf771", xlab=NULL, ylab=NULL,breaks = 30,xlim=c(0.25,0.46))
hist(qwe[[10]], las=1, main = "Porthos", xlab=NULL, ylab=NULL,breaks = 30,xlim=c(0.25,0.46))
hist(qwe[[11]], las=1, main = "vB_EfaM_A2", xlab=NULL, ylab=NULL,breaks = 30,xlim=c(0.25,0.46))
hist(qwe[[12]], las=1, main = "vB_OCPT_Ben", xlab=NULL, ylab=NULL,breaks = 30,xlim=c(0.25,0.46))
#####################################################################

'''

import glob
import itertools
import os
import pathlib
import re


GC_content_values = []
list_of_local_GCVs = []
entrycount = 0

my_path = os.getcwd()
files = glob.glob(my_path + '/**/*.cds', recursive=True)

for f in files:
    local_GC_content_values = [re.findall(r'\w+', os.path.basename(f))[0]]
    with open (f) as inf:
        allseqs = []
        rawlines = inf.readlines()
        lines = []
        applicant = ''
        letts = ''
        d = 0
        for g in rawlines:
            if re.findall(r'\w', g):
                if '>' in g:
                    entrycount += 1
                    if d != 0:
                        allseqs.append(applicant.strip())
                        allseqs.append(letts)
                        letts = ''
                    applicant = g
                    d += 1
                else:
                    letts += g.strip()
        allseqs.append(applicant.strip())
        allseqs.append(letts)

        runner = 0                    
        while runner < len(allseqs):
            if allseqs[runner].startswith('>'):
                GC_content_values.append(len(re.findall(r'[GC]', allseqs[runner+1].strip()))/len(allseqs[runner+1].strip()))
                local_GC_content_values.append(len(re.findall(r'[GC]', allseqs[runner+1].strip()))/len(allseqs[runner+1].strip()))
                if len(re.findall(r'[GC]', allseqs[runner+1]))/len(allseqs[runner+1]) == 0:
                    print(os.path.basename(f), end = '')
                    print(': zero GC content value in', re.findall(r'\S+', allseqs[runner][1:])[0])
            runner += 2
    list_of_local_GCVs.append(local_GC_content_values)

with open ('GC_content_values_all_seqs.txt', 'w') as ouf:
    for i in GC_content_values:
        ouf.write(str(i))
        ouf.write('\n')
with open  ('GC_content_values_by_files.txt', 'w') as ouf:
    transposed_list = map(list, itertools.zip_longest(*list_of_local_GCVs, fillvalue='NA'))
    for i in transposed_list:
        for j in i:
            ouf.write(str(j))
            ouf.write('\t')
        ouf.write('\n') 

print('\n', entrycount, 'protein-coding DNA sequences')
print('', len(GC_content_values), 'values in GC_content_values_all_seqs.txt')