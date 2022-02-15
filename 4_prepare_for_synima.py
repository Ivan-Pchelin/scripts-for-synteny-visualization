'''
The script performs formatting of Prokka genome annotation
software output for the use by Synima synteny visualization
package

by Ivan Pchelin, arcella.oraia@gmail.com
2022-02-10
'''


import glob
import os
import pathlib
import re
import sys

# This renames raw Prokka files
my_path = os.getcwd()
files = glob.glob(my_path + '/**/*.*', recursive=True)
for f in files:
    if f.endswith('faa'):
        os.rename(f, f[:-3]+'annotation.pep')
    if f.endswith('ffn'):
        os.rename(f, f[:-3]+'annotation.cds')
    if f.endswith('gff'):
        os.rename(f, f[:-3]+'annotation.gff3')
    if f.endswith('fasta'):
        os.rename(f, f[:-5]+'genome.fa')

# This removes all unnecessary files except for stupid MacOS system files
trigger = 'no'
files = glob.glob(my_path + '/**/*.*', recursive=True)
for f in files:
    if 'annotation' not in f and 'genome' not in f:
        if '.py' not in f and 'Repo_spec' not in f:
            trigger = 'yes'
if trigger == 'yes':
    print('\nThis script will remove all files from the folder and sub-folders except for')
    print('those necessary for Synima analysis.')
    print('Do you really have nothing useful here? y/n/a\n')
    reply = str(input())
    if reply.strip() == 'n':
        print('So please save your files in other location and re-run the script')
        sys.exit()
    elif reply.strip() == 'y':
        print('\nYou are about to delete your files in the folder and sub-folders.')
    elif reply.strip() == 'a':
        sys.exit()
    elif 'y' or 'n' not in reply:
        while 'n' or 'y' or 'a' not in reply:
            print(" 'y', 'n' or 'a' can be read")
            reply = str(input())
            if reply.strip() == 'n':
                decision_af = 'n'
                break
            if reply.strip() == 'y':
                decision_af = 'y'
                break
            if reply.strip() == 'a':
                sys.exit()
    print('Type "I understand."')
    while 'I understand.' not in reply:
        reply = str(input())
        if reply.strip() == 'I understand.':
            break
    for f in files:
        if 'annotation' not in f and 'genome' not in f:
            if '.py' not in f and 'Repo_spec' not in f:
                try: # This will remove files but not folders
                    os.remove(f)
                except:
                    pass
                
sequencenames = set()
files = glob.glob(my_path + '/**/*.*', recursive=True)
for f in files:
    if f.endswith('cds') or f.endswith('pep'):
        with open (f) as inf:
            lines = inf.readlines()
        with open (f, 'w') as ouf:
            for i in lines:
                if '>' not in i:
                    ouf.write(i)
                else:
                    if i[0:5] == '>cds-':
                        ouf.write(i)
                    else:
                        ouf.write('>cds-'+i[1:])
    if f.endswith('gff3'):
        with open (f) as inf:
            lines = inf.readlines()
        with open (f, 'w') as ouf:
            filename = os.path.basename(f)
            sequencename = re.split(r'\.',filename)[-3]
            sequencenames.add(sequencename)
            for i in lines:
                if len(re.findall(r'\w+', i)) > 1:
                    if '#' not in i and '>' not in i:
                        if re.findall('[^ATGC]', i.strip()):
                            stuff = re.split(r'\t', i)
                            stuff[1] = sequencename
                            stuff[2] = 'gene'
                        for i in stuff:
                            ouf.write(i)
                            if '\n' not in i:
                                ouf.write('\t')

# Create a global set with entries from PEP files
pep_files = glob.glob(my_path + '/**/*.pep', recursive=True)
cds_names = set()
for i in pep_files:
    with open (i) as inf:
        lines = inf.readlines()
    for l in lines:
        if l.startswith('>cds-'):
            cds_names.add(re.split(r' ', l)[0][5:])

# Delete from CDS files all entries missing from PEP files
for f in files:
    if '.py' not in f and 'Repo_spec' not in f:
        if f.endswith('cds'):
            with open (f) as inf:
                allseqs = []
                rawlines = inf.readlines()
            with open (f, 'w') as ouf:
                lines = []
                applicant = ''
                letts = ''
                d = 0
                for g in rawlines:
                    if re.findall(r'\w', g):
                        if '>' in g:
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
                        if re.findall(r'\S+', allseqs[runner])[0][5:] in cds_names:
                            ouf.write(allseqs[runner])
                            ouf.write('\n')
                            ouf.write(allseqs[runner+1])
                            ouf.write('\n')
                    runner += 2
print('\n CDS files are done')

# Delete from GFF3 files all entries missing from PEP files
gff_files = glob.glob(my_path + '/**/*.gff3', recursive=True)
for gff in gff_files:
    with open (gff) as inf:
        rawlines = inf.readlines()
    with open (gff, 'w') as ouf:
        for raw in rawlines:
            if len(re.findall(r'\w', raw)) > 2:
                for cds in cds_names:
                    if cds in re.split(r';', raw)[0]:
                        outentry = re.split(r'\t', raw)
                        if outentry[8][0:7] != 'ID=cds-':
                            outentry[8] = 'ID=cds-' + outentry[8][3:]
                        a = 0
                        while a < len(outentry):
                            ouf.write(outentry[a])
                            if a < len(outentry) - 1:
                                ouf.write('\t')
                            a += 1
print('\n GFF3 files are done')

# This is generate_Repo_spec.py
my_path = os.getcwd()
files = glob.glob(my_path + '/**/*.*', recursive=True)

genomes = {os.path.basename(i)[:-10] for i in files
 if i.endswith('fa')}

with open ('Repo_spec.txt', 'w') as ouf:
    ouf.write('//')
    for i in genomes:
        ouf.write('\n')
        ouf.write('Genome ')
        ouf.write(i)
        ouf.write('\n')
        ouf.write('Annotation ')
        ouf.write(i)
        ouf.write('\n')
        ouf.write('//')

print('\n Repo_spec.txt was generated')

print('\n Will Synima run with genes or contigs? Please type "genes" or "contigs"')
reply = str(input())
if reply.strip() == 'genes':
    genes_or_contigs = '-g g' # -g gene synteny (contigs by default)
elif reply.strip() == 'contigs':
    genes_or_contigs = ''
elif 'genes' or 'contigs' not in reply:
    while 'genes' or 'contigs' not in reply:
        print('Cannot understand')
        reply = str(input())
        if reply.strip() == 'genes':
            genes_or_contigs = '-g g'
            break
        if reply.strip() == 'contigs':
            genes_or_contigs = ''
            break

# Create a file with Synima instructions
#perl ../util/Blast_grid_all_vs_all.pl -r Repo_spec.txt -e 0.0001   #-t CDS (PEP by default)    
with open ('synima_instructions.txt', 'w') as ouf:
    ouf.write('perl ../util/Create_full_repo_sequence_databases.pl -r Repo_spec.txt -f gene ; ')
    ouf.write('perl ../util/Blast_grid_all_vs_all.pl -r Repo_spec.txt -e 0.0001 ; ')
    ouf.write('perl ../util/Blast_all_vs_all_repo_to_OrthoMCL.pl -r Repo_spec.txt ; ')
    ouf.write('perl ../util/Orthologs_to_summary.pl -o all_orthomcl.out ; ')
    ouf.write('perl ../util/DAGchainer_from_gene_clusters.pl -r Repo_spec.txt -c GENE_CLUSTERS_SUMMARIES.OMCL/GENE_CLUSTERS_SUMMARIES.clusters ; ')
    ouf.write('perl ../SynIma.pl -a Repo_spec.txt.dagchainer.aligncoords -b Repo_spec.txt.dagchainer.aligncoords.spans ' + genes_or_contigs)


print('\n synima_instructions.txt was generated')
print('\n To get your sequences in a pre-defined order, run\n perl ../SynIma.pl ', end='')
print('-a Repo_spec.txt.dagchainer.aligncoords -b Repo_spec.txt.dagchainer.aligncoords.spans -g g -x seq1,seq2,seq3')