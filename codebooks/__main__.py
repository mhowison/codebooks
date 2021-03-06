#!/usr/bin/env python
import argparse
import os
import pandas as pd
import sys
from codebooks import htmlbook

parser = argparse.ArgumentParser(prog="codebooks")
parser.add_argument("dataset")
parser.add_argument("--sep", "-s")
parser.add_argument("--output", "-o")
parser.add_argument("--desc", "-d")
args = parser.parse_args()

if args.dataset == "-":
    args.dataset = sys.stdin
    title = "Codebook"
else:
    title = "Codebook for " + os.path.basename(args.dataset)

read_args = {}
if args.sep:
    read_args["sep"] = args.sep

if args.desc:
    desc = pd.read_csv(args.desc, index_col=0).iloc[:, 0].fillna("").to_dict()
else:
    desc = {}

df = pd.read_csv(args.dataset, low_memory=False, **read_args)

if args.output:
    htmlbook(df, title=title, outfile=args.output, desc=desc)
else:
    print(htmlbook(df, title=title, desc=desc))
