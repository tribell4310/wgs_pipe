"""

depth_plots.py

Take in text-based read depth, plot depth along each chromosome, and output regions of interest where there is no coverage.

"""


import sys
from os import listdir
from os.path import isfile, join
import os
import matplotlib as mpl
mpl.use("Agg")
mpl.rc('figure', max_open_warning = 0)
import matplotlib.pyplot as plt


def main(prefix):
	# Load and filter relevant files
	onlyfiles = [f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(), f))]
	relevantfiles = []
	for eachfile in onlyfiles:
		if prefix in eachfile:
			if "_chr" in eachfile:
				relevantfiles.append(eachfile)
	print("Identified "+str(len(relevantfiles))+" files with prefix "+prefix+".")

	# Parse, scan, plot
	for item in relevantfiles:
		print("Plotting "+no_ext(str(item))+" ...")
		# Load file to memory
		f = open(item, "r")
		lines = f.readlines()
		f.close()

		# Transfer data to array
		x = []
		y = []
		counter = 1
		for line in lines:
			comps = line.replace("\n", "").split("\t")
			this_x = int(comps[1])
			this_y = int(comps[2])
			while this_x != counter:
				x.append(counter)
				y.append(0)
				counter += 1
			x.append(this_x)
			y.append(this_y)
			counter += 1

		# Make sure data is complete
		#x_new = [x[0]]
		#y_new = [y[0]]
		#for i in range(1, max(x)):
		#	if i not in x:
		#		x_new.append(i)
		#		y_new.append(0)
		#	else:
		#		my_pos = x.index(i)
		#		x_new.append(x[my_pos])
		#		y_new.append(y[my_pos])

		# Scan for regions where there is no coverage
		zeroes = []
		for i in range(0, len(x)):
			if y[i] == 0:
				zeroes.append(x[i])

		# Write out the zeroes file
		g = open(no_ext(item)+"_zeroes.tsv", "w")
		for zero in zeroes:
			g.write(str(zero)+"\n")
		g.close()

		# Create a plot of coverage versus chr position
		fig, ax = plt.subplots()
		ax.set(xlabel="Position in chromosome", ylabel="Coverage Depth")
		ax.grid()
		ax.set_yscale("symlog")
		ax.scatter(x, y)
		fig.savefig(no_ext(item)+"_coverage.png")
		plt.clf()
		if no_ext(str(item))[-6:] == "_chrXI":
			fig, ax = plt.subplots()
			ax.set(xlabel="Position in chromosome", ylabel="Coverage Depth")
			ax.grid()
			ax.set_yscale("symlog")
			ax.set_xlim([468000, 472000])
			ax.scatter(x, y)
			fig.savefig(no_ext(item)+"_coverage_Mic60.png")
			plt.clf()

	print("...done.")


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
	if len(sys.argv) >= 2:
		main(sys.argv[1])
	else:
		print("Usage: python foo.py file_prefix")
		exit()