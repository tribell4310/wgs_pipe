# wgs_pipe
Automated pipeline for paired-end WGS data analysis

Tristan Bell

## Use case

Paired-end illumina sequencing data for alignment onto a fasta-formatted reference genome.


## Dependencies

The data processing scripts require python 3.x with matplotlib installed (`python -m pip install matplotlib`).  The scripts should be placed into a dedicated working directory. Other dependencies are:
 - [bwa](https://bio-bwa.sourceforge.net/)
 - [samtools](http://www.htslib.org/)
 - [bcftools](https://samtools.github.io/bcftools/bcftools.html)

The scripts expect to find the bwa executable in `/usr/local/bwa/bwa`.  If yours is somewhere else, you'll need to symlink it there.

## Organize pairs of sequences

Paired-end sequencing data is usually returned from the sequencer as two .fastq.gz files with R1 and R2 labels.  Sequences can also be spread across multiple lanes that need to be merged.  We'll start by organizing this data for processing.

 - Run the first python script: `python wgs_pipe_py1.py`
 - This will return a `paired_reads.csv` file containing all .fastq.gz files found in your working directory.
 - Organize the files in the csv file so your paired reads are side by side, and sets are adjacent if they should be merged.

### Example

 - We want to process two samples.  One sample (TBb6-1) was sequenced on a single lane, but the other (MEb1-2) was sequenced across two lanes.
 - The csv output of `wgs_pipe_py1.py` looks like this:

`MEb1-2_S48_L001_R1_001.fastq.gz`  
`MEb1-2_S48_L001_R2_001.fastq.gz`  
`TBb6-1_S29_L001_R1_001.fastq.gz`  
`TBb6-1_S29_L001_R2_001.fastq.gz`  
`TBb6-1_S29_L002_R1_001.fastq.gz`  
`TBb6-1_S29_L002_R2_001.fastq.gz`  

 - We need to reformat it like this:

`MEb1-2_S48_L001_R1_001.fastq.gz,MEb1-2_S48_L001_R2_001.fastq.gz`  
`TBb6-1_S29_L001_R1_001.fastq.gz,TBb6-1_S29_L001_R2_001.fastq.gz,TBb6-1_S29_L002_R1_001.fastq.gz,TBb6-1_S29_L002_R2_001.fastq.gz`  


## Process the sequences

Now that the files are organized, we can align to a reference genome and perform analysis.

 - Run the second python script, specifying the reference genome for alignment and the max number of threads you want to give to the alignment processes: `python wgs_pipe_py1.py --ref ref.fa --max_threads 8`
 - Run the output bash script to start the pipeline: `bash RUNME.sh`

## Outputs

 - Aligned reads (*_mapped.bam)
 - Indexed aligned reads (*_mapped.bai)
 - Variant SNP calls against reference genome (*.var.bcf)
 - Table of SNP calls with %QUAL>20 (*_sig_snp.tsv)
 - Depth coverage across each chromosome (*.coverage)
 - Plots of coverage across each chromosome (*.png)


## Changing the scripts

 - The defined chromosomes for the coverage plots are currently hardcoded for yeast in the `split_coverage_3.sh` script.  If you are using a different system, change the chromosome labels here.


## Questions

For any problems, please open an issue ticket in this github repo, or contact me directly: tribell4310 [at] gmail [dot] com.

> Written with [StackEdit](https://stackedit.io/).
