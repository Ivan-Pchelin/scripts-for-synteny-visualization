'''
2022-02-10 by Ivan Pchelin
'''

import os
import re
import sys

print('\nThe script works with a FASTA file. It will write individual')
print('sequences to their own files in individual folders and generate')
print('the commands for Prokka software.')


# This defines the questionnaire
def youtalktoomuch():
    global decision
    reply = str(input())
    if reply.strip() == 'y':
        decision = 'y'
    elif reply.strip() == 'n':
        decision = 'n'
    elif reply.strip() == 'a':
        sys.exit()
    else:
        while 'y' or 'n' or 'a' not in reply:
            print("\n'y' or 'n' can be read")
            reply = str(input())
            if reply.strip() == 'y':
                decision = 'y'
                break
            if reply.strip() == 'n':
                decision = 'n'
            if reply.strip() == 'a':
                sys.exit()
    return (decision)

# This searches working directory for FASTA files.
current_dir = os.getcwd()
files = [f for f in os.listdir(current_dir) if f.endswith('.fasta')
 or f.endswith('.fa') or f.endswith('.fst') or f.endswith('.fas')]
if len(files) == 0:
    print("\n Didn't find FASTA files in the folder.")
    sys.exit()

options = ''

print ("\nLet's describe Prokka's job\n")
list_of_options_kingdom = ['Archaea', 'Bacteria', 'Mitochondria', 'Viruses'] 
k=1
for i in list_of_options_kingdom:
    print('(',end='')
    print( k, end='')
    print(')', i)
    k+=1
print('\n Which kingdom?')
options += '--kingdom ' + list_of_options_kingdom[int(input())-1]

print('\nShould tRNAs and rRNAs be annotated? y/n')
youtalktoomuch()
if decision == 'n':
    options += ' --norrna --notrna'

print('\nWill write the following options. Okay? y/n')
print(options)

youtalktoomuch()
if decision == 'n':
    sys.exit()

# This prints the names of FASTA files
k=1
print('\n')
for i in files:
    print('(',end='')
    print( k, end='')
    print(')', i)
    k+=1

# Specify nucleotide sequence files to work with
activefile = ''
print('Which file contains the genomes?')
activefile += files[int(input())-1]

# This is "hash_fasta.py"
with open (activefile) as inf:
# This will create nested list with the sequences
    stuff = []
    applicant = []
    k = 0
    line = inf.readline()
    while line:
        if '>' in line:
            if k == 1:
                stuff.append(applicant)
            k = 1
            applicant = []
            applicant.append(line)
        else:
            applicant.append(line)
        line = inf.readline()
    if not line:
        stuff.append(applicant)

my_path = os.getcwd()
my_new_folder = my_path + '/' + re.split(r'\.', activefile)[0] + '_dataset'
try:
    os.mkdir(my_new_folder)
except:
    pass

directories = []
for i in stuff:
    directories.append(re.findall(r'\S+', i[0])[0][1:])
    currentname = re.findall(r'\S+', i[0])[0][1:] + '.fasta'
    current_outfolder = my_new_folder + '/' + re.findall(r'\S+', i[0])[0][1:]
    os.mkdir(current_outfolder)
    with open(current_outfolder + '/' + currentname, 'w') as ouf:
        for j in i:
            ouf.write(j)
#print(directories)
#sys.exit()

# Create a file with Prokka instructions
with open ('prokka_instructions.txt', 'w') as ouf:
    not_first = False
    for i in directories:
        if not_first:
            ouf.write(' ; ')
        not_first = True
        folder = (re.split(r'\.', activefile)[0] + '_dataset/' + i)
        ouf.write('./prokka ' + options + ' --cpus 0 --force --quiet --outdir ' + folder + ' --prefix '+ i + ' ' + folder + '/' + i + '.fasta')

print ('\nThe dataset is in the folder', re.split(r'\.', activefile)[0] + '_dataset.')
print ('Check prokka_instructions.txt for the Prokka commands.')
print ('The commands should work from /prokka/bin with the folder with data located at the same place.')