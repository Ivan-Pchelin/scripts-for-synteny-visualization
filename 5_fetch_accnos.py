# The script fetches accession numbers from all FASTA file in the folder
# 2021-10-06

# Malfunctions when sequence names contain full stops
# Some sequences get missing

import os
import re
import sys

# Extract taxonomy from taxonomy.xml or don't. Requires also taxids.txt
# produced by extract_taxid.py
# Taxonomic information can be fetched with the use of EFetch utility
# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=taxonomy&id=...,...,...

current_dir = os.getcwd()
justcurious = [f for f in os.listdir(current_dir) if f.endswith('.txt') or f.endswith('.xml')]
if 'taxonomy.xml' and 'taxids.txt' in justcurious:
    print('\n Extract taxonomy? y/n/a')
    reply = str(input())
    if reply.strip() == 'n':
        decision_et = 'n'
    elif reply.strip() == 'y':
        decision_et = 'y'
    elif reply.strip() == 'a':
        sys.exit()
    elif 'y' or 'n' not in reply:
        while 'n' or 'y' or 'a' not in reply:
            print(" 'y', 'n' or 'a' can be read")
            reply = str(input())
            if reply.strip() == 'n':
                decision_et = 'n'
                break
            if reply.strip() == 'y':
                decision_et = 'y'
                break
            if reply.strip() == 'a':
                sys.exit()
else:
    decision_et = 'n'

# This searches working directory for FASTA files
files = [f for f in os.listdir(current_dir) if f.endswith('.fasta')
 or f.endswith('.fa') or f.endswith('.fst') or f.endswith('.fas')]
if len(files) == 0:
    print("\n Didn't find FASTA files in the folder.")
    sys.exit()

found_accessions = set()
outlist = []

for f in files:
    with open (f) as inf:
        line = inf.readline()
        while line:
            if line.startswith('>'):                
                found_accessions.add(re.split(r':', re.findall(r'\S+', line)[0])[0][1:])
            line = inf.readline()

for i in found_accessions:
    outlist.append(i)
outlist.sort()

# Prepare simple one-column table of sequence names
if decision_et == 'n':
    with open ('found_accessions.txt', 'w') as ouf:
        start = True
        for i in outlist:
            if start != True
                ouf.write(',')
            start = False
            ouf.write(i)
    print('\n', len(outlist), 'accessions were found')


# Supplement found accessions with taxonomic information
if decision_et == 'y':

# Check for the availability of TaxIDs for all sequences
    with open ('taxids.txt') as inf:
        taxids = inf.readlines()
    acc = set(re.findall(r'\S+', i)[0] for i in taxids)
    nam = set(re.findall(r'\S+', i)[1] for i in taxids)
    missing = set()
    for i in outlist:
        if re.split(r'\.', i)[0] not in acc:
            if i not in nam:
                missing.add(i)
    if missing != set():
        print ('\nMissing from taxids.txt entries:')
        for i in missing:
            print(i,' ')
        with open('missing_taxids.txt','w') as ouf:
            for i in missing:
                ouf.write(i)
                ouf.write('\n')
        print('\nCheck missing_taxids.txt') 
        sys.exit()

# If all found accessions have matches in taxids.txt, match names with taxIDs
    outdictwt = {i:re.findall(r'\S+', j)[2] 
    for i in outlist for j in taxids 
    if re.split(r'\.', i)[0] in re.findall(r'\w+', j)[0:2]}

# Supplement the dictionary with taxonomic information
    with open ('taxonomy.xml') as inf:
        taxonomy = inf.readlines()

    for i in outdictwt.keys():
        ti = outdictwt[i]
        runner = 0
        theplace = False
        while theplace != True:
            if re.findall(r'\S+', taxonomy[runner]):
                if ti in re.findall(r'\S+', taxonomy[runner])[0]:
                    theplace = True
            runner += 1

        while not taxonomy[runner].startswith('<Taxon>'):
            runner -= 1
        foundfamily = 0
        foundgenus = 0
        foundspecies = 0
        while 'CreateDate' not in taxonomy[runner]:
            if '<Rank>family' in taxonomy[runner]:
                family = re.split(r'ScientificName', taxonomy[runner-1])[1][1:-2]
                foundfamily = 1
            if '<Rank>genus' in taxonomy[runner]:
                genus = re.split(r'ScientificName', taxonomy[runner-1])[1][1:-2]
                foundgenus = 1
            if '<Rank>species' in taxonomy[runner]:
                if '<ScientificName>' in taxonomy[runner-1]:
                    species = re.split(r'ScientificName', taxonomy[runner-1])[1][1:-2]
                    foundspecies = 1
                if '<ScientificName>' in taxonomy[runner-2]:
                    species = re.split(r'ScientificName', taxonomy[runner-2])[1][1:-2]
                    foundspecies = 1
            runner += 1
        if foundfamily == 1:
            outdictwt[i] = outdictwt[i] + '\t' + family
        else:
            outdictwt[i] = outdictwt[i] + '\tND'
        if foundgenus == 1:
            outdictwt[i] = outdictwt[i] + '\t' + genus
        else:
            outdictwt[i] = outdictwt[i] + '\tND'
        if foundspecies == 1:
            outdictwt[i] = outdictwt[i] + '\t' + species
        else:
            outdictwt[i] = outdictwt[i] + '\tND'


# Write the taxonomy in outfile 
    with open ('found_accessions.txt', 'w') as ouf:
        ouf.write('Sequence\tTaxID\tFamily\tGenus\tSpecies\n')
        for t in outdictwt.keys():
            ouf.write(t)
            ouf.write('\t')
            ouf.write(outdictwt[t])
            ouf.write('\n')