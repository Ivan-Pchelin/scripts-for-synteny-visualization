# scripts-for-synteny-visualization
Here are some Python scripts needed to prepare nucleotide sequence data for analysis with the use of Prokka and Synima software

### Data preparation
1. Determine the range of genomes for which the analysis is being carried out. Using the full genome of interest in a MegaBLAST search, find similar sequences in the database. Download the desired genomes in FASTA format, all in one file.
2. *For circular genomes*, determine a common starting sequence. Graphic Summary of BLAST results may be helpful to approximately determine the coordinates of a region of homology. In the GenBank view mode, a protein-coding sequence in this region can be picked from one of the genomes and used in a BLAST search. The search results for this short sequence along with genomic FASTA are taken by **common_start.py** as input. The script is launched from the folder containing the files with sequences. It re-writes all genomic sequences so that they start from the determined homologous region. The script expects to find all short homologous fragments being oriented in the same direction.
3. **rename_fasta.py** can be used to rename the sequences in the file. The matches between accession numbers and names are written manually to rename.txt. The script is launched from the folder containing file with sequences and rename.txt. The latter is formatted in the following way:

```
>AP009390.1	>Enterococcus_phage_phiEF24C
>AP018714.1	>Enterococcus_phage_phiEF17H
```

### Analysis
1. **prepare_for_prokka.py** creates a folder tree and generates the commands for Prokka software. After this step, Prokka analysis is launched. https://github.com/tseemann/prokka
2. **prepare_for_synima.py** deletes everything except for itself and the files needed for Synima from the working folder and sub-folders. It also performs some formatting of the data. The instructions for Synima as well as Repo_spec.txt are generated. https://github.com/rhysf/Synima
3. To create a graph with the genomes aligned in a pre-defined order, the -x option is used at the final stage of Synima analysis. The list of FASTA headers to use with the option can be prepared by running **fetch_accnos.py**.

### GC-content
**global_GC_content.py** can be used to calculate the distribution of coding sequences according to their GC-content and **refine_annotations_by_GCV.py** prepares four partial datasets for Synima. If use refine_annotations_by_GCV.py, please set the interquartile boundaries within the code.
