import argparse
import codebooks
import os
import pandas as pd
import sys

def main():

    parser = argparse.ArgumentParser(description=codebooks.__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-v", "--version",
                        action="version",
                        version="codebooks {}".format(codebooks.__version__))
    parser.add_argument("dataset")
    parser.add_argument("--sep", "-s")
    parser.add_argument("--output", "-o")
    parser.add_argument("--desc", "-d")
    parser.add_argument("--na_values", "-?")
    parser.add_argument("--encoding", default="utf8")
    args = parser.parse_args()

    if args.dataset == "-":
        input_file = sys.stdin
        title = "Codebook"
    else:
        input_file = args.dataset
        title = "Codebook for " + os.path.basename(args.dataset)

    read_args = {}
    if args.sep:
        read_args["sep"] = args.sep

    if args.desc:
        desc = pd.read_csv(args.desc, index_col=0).iloc[:, 0].fillna("").to_dict()
    else:
        desc = {}

    if args.na_values:
        read_args["na_values"] = args.na_values.split(",")

    df = pd.read_csv(input_file, low_memory=False, encoding=args.encoding, **read_args)

    if args.output:
        codebooks.htmlbook(df, title=title, outfile=args.output, desc=desc)
    elif args.dataset == "-":
        print(codebooks.htmlbook(df, title=title, desc=desc))
    else:
        outfile = os.path.splitext(args.dataset)[0] + "_codebook.html"
        codebooks.htmlbook(df, title=title, outfile=outfile, desc=desc)

if __name__ == "__main__":
    sys.exit(main())
