#!/bin/python

import sys
import csv


def get_labels(infile):
    reader = csv.reader(infile, delimiter="\t")
    next(reader)
    for row in reader:
        print row[-1]
        # outfile.write(row[-1] + '\n')

if __name__ == "__main__":
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            get_labels(infile)
    else:
        print "Usage: " + sys.argv[0] + " <infile.tsv>"
