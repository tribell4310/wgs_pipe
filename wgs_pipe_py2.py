"""
wgs_pipe_py2.py

"""


import sys
import os
from os.path import isfile, join
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--ref", help="fasta-formated reference genome for alignment")
parser.add_argument("--max_threads", help="maximum threads for job runs")
args = parser.parse_args()


def main(args):
	ref = args.ref.strip()
	max_threads = args.max_threads.strip()

	# Find paired_reads.csv file
	wd = os.getcwd()
	if isfile(join(wd, "paired_reads.csv")):
		with open("paired_reads.csv", "r") as f:
			lines = f.readlines()
	else:
		print("No paired_reads.csv file detected in this directory.  Exiting...")
		exit()

	# Parse the lines into individual files
	blocks = []
	merge_flags = []
	for line in lines:
		items = line.strip().split(",")
		if len(items) % 2 != 0:
			print("Every line in paired_reads.csv should have an even number of files separated by commas - the R1/R2 pairs for each lane run on this dataset.  Please reformat.  Exiting...")
			exit()
		elif len(items) == 0:
			continue
		else:
			blocks.append(items)
			if len(items) == 2:
				merge_flags.append(False)
			else:
				merge_flags.append(True)

	# Write out a big bash script to run the pipeline
	with open("RUNME.sh", "w") as g:
		g.write("#!/bin/bash\n\n")
		g.write("/usr/local/bwa/bwa index "+ref+"\n")
		g.write("samtools faidx "+ref+"\n")
		for i in range(0, len(blocks)):
			g.write(bash_writer1(blocks[i], merge_flags[i], ref, max_threads)+"\n")
		for i in range(0, len(blocks)):
			g.write(bash_writer2(blocks[i], merge_flags[i], ref, max_threads)+"\n")

	# Report back to user
	print("\tDetected "+str(len(blocks))+" separate conditions for analysis.\n\t\tWill be aligned against "+ref+", which must be in this directory!\n\t\tOnce complete, run RUNME.sh.")

	
def bash_writer1(block, merge_flag, ref, max_threads):
	out_str = ""
	if merge_flag == False:
		out_str += "/usr/local/bwa/bwa mem -t "+max_threads+" "+ref+" "+block[0]+" "+block[1]+" > "+arb_no_ext(block[0], ".fastq.gz")+"_mapped.sam && "
		out_str += "samtools view -@ "+max_threads+" -S -b "+arb_no_ext(block[0], ".fastq.gz")+"_mapped.sam > "+arb_no_ext(block[0], ".fastq.gz")+"_mapped.bam && "
		out_str += "samtools sort -@ "+max_threads+" "+arb_no_ext(block[0], ".fastq.gz")+"_mapped.bam -o "+arb_no_ext(block[0], ".fastq.gz")+"_mapped.sorted.bam && "
		out_str += "bcftools mpileup -f "+ref+" "+arb_no_ext(block[0], ".fastq.gz")+"_mapped.sorted.bam > "+arb_no_ext(block[0], ".fastq.gz")+"_mapped.raw.bcf && "
		out_str += "samtools index "+arb_no_ext(block[0], ".fastq.gz")+"_mapped.sorted.bam && "
		out_str += "bcftools call --ploidy 1 -O b -vc "+arb_no_ext(block[0], ".fastq.gz")+"_mapped.raw.bcf > "+arb_no_ext(block[0], ".fastq.gz")+"_mapped.var.bcf && "
		out_str += "bcftools view -f '%QUAL>20' "+arb_no_ext(block[0], ".fastq.gz")+"_mapped.var.bcf > "+arb_no_ext(block[0], ".fastq.gz")+"_sig_snp.tsv "
	else:
		for i in range(0, int(len(block)/2)):
			out_str += "/usr/local/bwa/bwa mem -t "+max_threads+" "+ref+" "+block[(2*i)]+" "+block[(2*i)+1]+" > "+arb_no_ext(block[(2*i)], ".fastq.gz")+"_mapped.sam && "
		for i in range(0, int(len(block)/2)):
			out_str += "samtools view -@ "+max_threads+" -S -b "+arb_no_ext(block[(2*i)], ".fastq.gz")+"_mapped.sam > "+arb_no_ext(block[(2*i)], ".fastq.gz")+"_mapped.bam && "
		out_str += "samtools merge "+arb_no_ext(block[0], ".fastq.gz")+"_merge_mapped.bam "
		for i in range(0, int(len(block)/2)):
			out_str += arb_no_ext(block[(2*i)], ".fastq.gz")+"_mapped.bam "
		out_str += "&& "
		out_str += "samtools sort -@ "+max_threads+" "+arb_no_ext(block[0], ".fastq.gz")+"_merge_mapped.bam -o "+arb_no_ext(block[0], ".fastq.gz")+"_merge_mapped.sorted.bam && "
		out_str += "bcftools mpileup -f "+ref+" "+arb_no_ext(block[0], ".fastq.gz")+"_merge_mapped.sorted.bam > "+arb_no_ext(block[0], ".fastq.gz")+"_merge_mapped.raw.bcf && "
		out_str += "bcftools mpileup -f "+ref+" "+arb_no_ext(block[0], ".fastq.gz")+"_merge_mapped.sorted.bam > "+arb_no_ext(block[0], ".fastq.gz")+"_merge_mapped.raw.bcf && "
		out_str += "samtools index "+arb_no_ext(block[0], ".fastq.gz")+"_merge_mapped.sorted.bam && "
		out_str += "bcftools call --ploidy 1 -O b -vc "+arb_no_ext(block[0], ".fastq.gz")+"_merge_mapped.raw.bcf > "+arb_no_ext(block[0], ".fastq.gz")+"_merge_mapped.var.bcf && "
		out_str += "bcftools view -f '%QUAL>20' "+arb_no_ext(block[0], ".fastq.gz")+"_merge_mapped.var.bcf > "+arb_no_ext(block[0], ".fastq.gz")+"_merge_sig_snp.tsv "
	return out_str 


def bash_writer2(block, merge_flag, ref, max_threads):
	out_str = ""
	if merge_flag == False:
		out_str += "samtools depth "+arb_no_ext(block[0], ".fastq.gz")+"_mapped.sorted.bam > "+arb_no_ext(block[0], ".fastq.gz")+"_mapped.coverage && "
		out_str += "bash ./split_coverage_3.sh "+arb_no_ext(block[0], ".fastq.gz")+"_mapped.coverage && "
		out_str += "python depth_plots.py "+arb_no_ext(block[0], ".fastq.gz")+"_mapped "
	else:
		out_str += "samtools depth "+arb_no_ext(block[0], ".fastq.gz")+"_merge_mapped.sorted.bam > "+arb_no_ext(block[0], ".fastq.gz")+"_merge_mapped.coverage && "
		out_str += "bash ./split_coverage_3.sh "+arb_no_ext(block[0], ".fastq.gz")+"_merge_mapped.coverage && "
		out_str += "python depth_plots.py "+arb_no_ext(block[0], ".fastq.gz")+"_merge_mapped "
	return out_str


def arb_no_ext(filename, extension):
	""" Simple string find and replace. """
	idx = filename.find(extension)
	return filename[:idx]


def no_ext(inStr):
	"""
	Takes an input filename and returns a string with the file extension removed.

	"""
	prevPos = 0
	currentPos = 0
	while currentPos != -1:
		prevPos = currentPos
		currentPos = inStr.find(".", prevPos+1)
	return inStr[0:prevPos]


if __name__ == "__main__":
	if (args.ref == None) or (args.max_threads == None):
		print("Check usage.  Use python wgs_pipe_py2.py --help for all options.")
	else:
		main(args)