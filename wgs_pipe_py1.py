"""
wgs_pipe_py1.py

"""


import sys
import os
from os import listdir
from os.path import isfile, join
import argparse
parser = argparse.ArgumentParser()

args = parser.parse_args()


def main():
	# Find all .tar.gz files
	wd = os.getcwd()
	onlyfiles = [f for f in listdir(wd) if isfile(join(wd, f)) and join(wd, f).endswith(".fastq.gz")]
	
	# Write out to a csv one per line
	with open("paired_reads.csv", "w") as g:
		for file in onlyfiles:
			g.write(file.strip()+"\n")

	# Report out
	print("\tDetected "+str(len(onlyfiles))+" fastq.gz files in this directory.\n\t\tOrganize paired_reads.csv into pairs for merging.\n\t\tOnce complete, run wgs_pipe_py2.py.")
	



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
	main()