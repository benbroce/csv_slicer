#!/usr/bin/python3

# Slices columns from CSV file
# usage: csv_slicer.py [-h] [-c COLUMN] [-v] [-u] csv_file

import argparse
import requests
import tempfile


# argument parser
parser = argparse.ArgumentParser(description="Slices columns from CSV file.")
parser.add_argument("csv_file", help="CSV file to be parsed")
parser.add_argument("-c", metavar="COLUMN", type=int,
                    action="append", help="columns to select from CSV file")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="print logging messages")
parser.add_argument("-u", "--url", action="store_true",
                    help="read csv_file from url instead of local path")
args = parser.parse_args()


def process_file(file, args):
    # split columns and print
    for line in file:
        if args.verbose:
            print("COLS", args.c, end="\t")
        if args.c:
            columns = line.split(",")
            for column in args.c[:-1]:
                print(columns[column], end=", ")
            print(columns[args.c[-1]], end="\n")
        else:
            print(line, end="")
    print()
    return


# open data file
if args.url:
    # download csv file by url -> store in tempfile for processing
    if args.verbose:
        print("Requesting CSV file from URL:", args.csv_file, "\n")
    # default mode is binary, wrong format for processing (string here)
    with tempfile.TemporaryFile(mode="r+") as file:
        file.write(requests.get(args.csv_file, stream=True).text)
        file.seek(0)
        process_file(file, args)
else:
    # open file locally
    if args.verbose:
        print("Opening file locally at:", args.csv_file, "\n")
    with open(args.csv_file) as file:
        process_file(file, args)
