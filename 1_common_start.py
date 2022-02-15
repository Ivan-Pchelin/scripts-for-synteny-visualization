'''
2022-02-08 by Ivan Pchelin
'''
import re
import sys
import os

#################################################################################
############################# A COUPLE OF FUNCTIONS #############################
#################################################################################

# This defines the questionnaire
def youtalktoomuch():
    global decision
    reply = str(input())
    if reply.strip() == 'y':
        decision = 'y'
    elif reply.strip() == 'n':
        sys.exit()
    elif reply.strip() == 'a':
        sys.exit()
    else:
        if "don't know" in reply:
            print('\nI am sorry, man')
        while 'y' or 'n' or 'a' not in reply:
            print("\n'y' or 'n' can be read")
            reply = str(input())
            if reply.strip() == 'y':
                decision = 'y'
                break
            if reply.strip() == 'n':
                sys.exit()
            if reply.strip() == 'a':
                sys.exit()
    return(decision)

def complement(sequence):
    sequence = sequence.upper()
    c_sequence = sequence[::-1]
    c_sequence = c_sequence.replace('A', 'F').replace('T', 'A').replace('F', 'T')
    c_sequence = c_sequence.replace('G', 'F').replace('C', 'G').replace('F', 'C')
    c_sequence = c_sequence.replace('M', 'F').replace('K', 'M').replace('F', 'K')
    c_sequence = c_sequence.replace('R', 'F').replace('Y', 'R').replace('F', 'Y')
    c_sequence = c_sequence.replace('V', 'F').replace('B', 'V').replace('F', 'B')
    c_sequence = c_sequence.replace('H', 'F').replace('D', 'H').replace('F', 'D')
    return (c_sequence)

# Re-write all sequences in single lines
def into_a_single_line(activefile):
    allseqs = []
    lines = []
    applicant = ''
    letts = ''
    d = 0
    with open (activefile) as inf:
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
    return(allseqs)


#################################################################################
################################### QUESTIONS ###################################
#################################################################################

# This searches working directory for FASTA files.
current_dir = os.getcwd()
files = [f for f in os.listdir(current_dir) if f.endswith('.fasta')
 or f.endswith('.fa') or f.endswith('.fst') or f.endswith('.fas')]
if len(files) == 0:
    print("\n Didn't find FASTA files in the folder.")
    sys.exit()

print('\nThis script works with two FASTA files, one with circular genomes')
print('and another with BLAST results. It will re-write long sequences from')
print('the first file so that each will start from the short sequences from the second file.')

print('\nAre your genomes circular? y/n')
youtalktoomuch()
if decision == 'n':
    sys.exit()

print('\nAre your short sequences oriented in the same direction? y/n')
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
print('\n Which file contains the genomes?')
activefile += files[int(input())-1]
starts = ''
print('\n Which file contains the common fragments?')
starts += files[int(input())-1]

# Re-write the sequences as single lines.
# Genomes are in a list; fragments are in a dictionary
plain_genomes = into_a_single_line(activefile)
start_sequences_init0 = into_a_single_line(starts)
# Remove C_-s from the beginnings of the names of complemented sequences
start_sequences_list = []
for i in start_sequences_init0:
    if i.startswith('>C_'):
        start_sequences_list.append('>'+i[3:])
    else:
        start_sequences_list.append(i)

a = [re.split(':', re.findall(r'\S+', i)[0])[0][1:] 
     for i in start_sequences_list if i.startswith('>')]
b = [i for i in start_sequences_list if not i.startswith('>')]
start_sequences_dictionary = dict(zip(a, b))


# Ensure all the sequences in the file with genomes have their
# matches in BLAST results
genomic_sequences = {re.findall(r'\S+', i)[0][1:] for i in plain_genomes if i.startswith('>')}
missing = {i for i in genomic_sequences if i not in start_sequences_dictionary.keys()}
if missing != set():
    print ('\nCould not find BLAST results for the following genomes in', starts, end='')
    print (':\n')
    with open ('missing_fragments.txt', 'w') as ouf:
        for i in missing:
            print (i)
            ouf.write (i)
            ouf.write ('\n')
    print ('\ncheck missing_fragments.txt for the list')


#################################################################################
################################### MAIN PART ###################################
#################################################################################

# This writes the final file with rotated genomes
with open ('re-written_' + activefile, 'w') as ouf:
    runner = 0
    while runner < len(plain_genomes):
        ouf.write(plain_genomes[runner])
        ouf.write('\n')
        sequence = plain_genomes[runner+1]
        c_sequence = complement(sequence)
        probe = start_sequences_dictionary[re.findall(r'\S+', plain_genomes[runner][1:])[0]]
        c_probe = complement(probe)
        if probe in sequence:
            probe_start = [m.start() for m in re.finditer(probe, sequence)][0]
            ouf.write(sequence[probe_start:])           
            ouf.write(sequence[:probe_start])
        elif c_probe in sequence:
            probe_start = [m.start() for m in re.finditer(probe, c_sequence)][0]
            ouf.write(c_sequence[probe_start:])           
            ouf.write(c_sequence[:probe_start])
        else:
            print ('Could not match a fragment of', plain_genomes[runner], 'with the genome')
            sys.exit()
        ouf.write('\n')
        runner += 2