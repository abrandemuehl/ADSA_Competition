#!/bin/python
import sys
import random


def count_lines(filename):
    count = 0
    with open(filename, 'r') as file:
        for line in file:
            count += 1
    return count


def print_lines(infile):
    for i in range(count_lines(infile)):
        print random.randint(0, 1)


if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        print_lines(sys.argv[1])
    else:
        print "Usage: " + sys.argv[0] + " <infile>"
        


