# Codebooks

Automatically generate codebooks from dataframes. Includes methods to:
* Infer variable type (as unique key, indicator, categorical, or continuous).
* Summarize values with histograms and KDEs.
* Generate a self-contained HTML report (may be extended to PDF or other formats in the future).

Usage:

    codebooks -o output.html input.csv

## Example

![Screenshot of codebook for test dataset](https://raw.githubusercontent.com/mhowison/codebooks/dev/doc/screenshot.png)

## Adding variable descriptions

You can specify a csv file that maps variable names to descriptions using:

    codebooks --desc descriptions.csv -o output.html input.csv

The csv file is expected to have two columns (variable, description).

## License

3-Clause BSD (see LICENSE)

## Tests

The `test/` subdirectory contains a script to generate a synthetic data set, an integration test for the codebooks package, and a benchmark script used to test performance optimizations. You can run these with:

    cd test
    python dataset.py
    codebooks --desc desc.csv dataset.csv
    codebooks --desc desc.csv --parquet dataset.parquet
    python benchmark.py

## Authors

Mark Howison  
[http://mark.howison.org](http://mark.howison.org)
