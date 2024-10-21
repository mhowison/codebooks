import argparse
import codebooks
import codebooks.html
import os
import sys
from codebooks import log
from pandas import DataFrame, read_csv, read_parquet


def main():

    parser = argparse.ArgumentParser(
        description=codebooks.__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="codebooks {}".format(codebooks.__version__)
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="suppress progress bars and info messages",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="show all logging messages, including debugging output",
    )
    parser.add_argument(
        "dataset",
        help="""
            Path to the input dataset in tabular format
            (or Parquet format with --parquet).
        """
    )
    parser.add_argument(
        "--sep",
        "-s",
        help="Tabular format separator [uses pandas.read_csv default value]."
    )
    parser.add_argument(
        "--encoding",
        "-e",
        help="""
            Tabular format file encoding [uses pandas.read_csv default value].
        """
    )
    parser.add_argument(
        "--na",
        "-?",
        help="""
            Tabular format comma-separated list of strings to convert to NaN
            [uses pandas.read_csv default value].
        """
    )
    parser.add_argument(
        "--parquet",
        "-p",
        action="store_true",
        help="Use Parquet format instead of tabular."
    )
    parser.add_argument(
        "--desc",
        "-d",
        help="""
            Path to a CSV data dictionary file with columns 'variable' and
            'description' [optional].
        """
    )
    parser.add_argument(
        "--output",
        "-o",
        help="""
            Path to the output HTML codebook file
            [default: dataset filename with '_codebook.html' appended].
        """
    )

    args = parser.parse_args()

    if args.debug:
        log.setLevel(log.DEBUG)
    elif args.quiet:
        log.setLevel(log.ERROR)
    else:
        log.setLevel(log.INFO)

    if args.dataset == "-":
        input_file = sys.stdin
        title = "Codebook"
    else:
        input_file = args.dataset
        title = "Codebook for " + os.path.basename(args.dataset)

    read_args = {}
    if args.sep:
        read_args["sep"] = args.sep
    if args.encoding:
        read_args["encoding"] = args.encoding
    if args.na:
        read_args["na_values"] = args.na.split(",")

    if args.desc:
        desc = (
            read_csv(args.desc, usecols=["variable", "description"])
            .set_index("variable")
            .fillna("")
            .to_dict()
        )
        desc = desc['description']
    else:
        desc = {}

    log.info("reading input file")
    if args.parquet:
        df: DataFrame = read_parquet(input_file)
    else:
        df: DataFrame = read_csv(input_file, low_memory=False, **read_args)

    log.info("generating codebook")
    if args.output:
        codebooks.html.generate(
            df,
            title=title,
            outfile=args.output,
            desc=desc
        )
    elif args.dataset == "-":
        print(
            codebooks.html.generate(
                df,
                title=title,
                desc=desc
            )
        )
    else:
        outfile = os.path.splitext(args.dataset)[0] + "_codebook.html"
        codebooks.html.generate(
            df,
            title=title,
            outfile=outfile,
            desc=desc
        )


if __name__ == "__main__":
    main()
