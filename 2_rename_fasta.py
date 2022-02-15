'''
This script renames sequences in FASTA file format.
It reads the file 'rename.txt', where each line starts from
original name of a sequence, maybe incomplete.
What follows original name after a space in 'rename.txt',
is used as a start of amended sequence name in new file. 

By Ivan Pchelin, arcella.oraia@gmail.com, 2021-10-06
'''

#------------------------------------------
#------------------------------------------
# Do you need your sequences sorted? 'Yes'/'No'
ssorted = 'Yes'

# The length of clue: 'full'/'7'
cluelength = 'full'

# If the cluelength = '7', ALL NAMES MUST BE
# UNIQUE WITHIN FIRST SEVEN SYMBOLS
#------------------------------------------
#------------------------------------------

import os
import re
import sys


# This will read file with instructions how to rename
with open ('rename.txt') as inf:
    howtochangenames = inf.readlines()
# This will create a dictionary with renaming instructions
dictionary = dict()
if cluelength == '7':
    clues = [re.findall(r'\S+', x)[0][:6] for x in howtochangenames]
if cluelength == 'full':
    clues = []
    for i in howtochangenames:
        clues.append(re.split(r'\.', re.findall(r'\S+', i)[0])[0])
values = [re.findall(r'\S+', x)[1] for x in howtochangenames]
i = 0
while i < len(clues):
    dictionary[clues[i]] = values[i]
    i += 1


# This searches working directory for FASTA files
current_dir = os.getcwd()
files = [f for f in os.listdir(current_dir) if f.endswith('.fasta')
 or f.endswith('.fa') or f.endswith('.fst')]
if len(files) == 0:
    print("\n Didn't find FASTA files in the folder.")
    sys.exit()

# Re-write all sequences in single lines
for runner in files:
    with open ('renamed_' + runner[:len(runner)-len(re.findall(r'\w+$',
             runner)[0])-1] + '.fas', 'w') as ouf:
        lines = []
        applicant = ''
        letts = ''
        d = 0
        with open (runner) as inf:
            allseqs = []
            rawlines = inf.readlines()
            for i in rawlines:
                if '>' not in i:
                    qwerty = i.replace('-', '')
                else:
                    qwerty = i
                lines.append(qwerty)
            for i in lines:
                if re.findall(r'\w', i):
                    if '>' in i:
                        if d != 0:
                            allseqs.append(applicant.strip())
                            allseqs.append(letts)
                            letts = ''
                        applicant = i
                        d += 1
                    else:
                        letts += i.strip()
            allseqs.append(applicant.strip())
            allseqs.append(letts)
        for i in allseqs:
            if i.startswith('>C_'):
                i = '>' + i[3:]
            if i.startswith('>'):
                if re.split(r'\.', re.findall(r'\S+', i)[0])[0] in clues:
                    ouf.write(dictionary.get(re.split(r'\.', re.findall(r'\S+', i)[0])[0]))
                else:
                    ouf.write(i)
                ouf.write('\n')
            else:
                ouf.write(i)
                ouf.write('\n')