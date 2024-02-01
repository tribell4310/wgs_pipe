#!/bin/bash

infile="$1"
echo ${infile}
for chrom in "chrI" "chrII" "chrIII" "chrIV" "chrV" "chrVI" "chrVII" "chrVIII" "chrIX" "chrX" "chrXI" "chrXII" "chrXIII" "chrXIV" "chrXV" "chrXVI" "chrM"
do
	outfile="${prefix}_${chrom}.coverage"
	awk -v mychrom=$chrom '$1 == mychrom {print $0}' ${infile} > ${outfile}
done
