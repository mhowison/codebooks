# Codebooks

Automatically generate codebooks from dataframes. Includes methods to:
* Infer variable type (as unique key, indicator, categorical, or continuous).
* Summarize values with histograms and KDEs.
* Generate a self-contained HTML report (may be extended to PDF or other formats in the future).

Usage:

    codebooks -o output.html input.csv

## Adding variable descriptions

You can specify a csv file that maps variable names to descriptions using:

    codebooks --desc descriptions.csv -o output.html input.csv

The csv file is expected to have two columns (variable name, description).

## License

3-Clause BSD (see LICENSE)

## Authors

Mark Howison  
[http://mark.howison.org](http://mark.howison.org)
