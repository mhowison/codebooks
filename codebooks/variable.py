import pandas as pd

def _range(series):
    x = series.sort_values()
    n = len(x)
    return (x[0], x[int(0.25*n)], x[int(0.5*n)], x[int(0.75*n)], x[n-1])

class Variable(obj):

    def __init__(self, series):
        """
        """
        if not isinstance(series, pd.Series):
            raise ValueError("variable must be a pandas series object")

        self.length = len(series)
        self.missing = series.isnull()

        # Determine variable type
        if series.is_unique:
            self.type = "Unique Key"
            self.distinct = self.length - self.missing.sum()
            self.dense = (self.length == self.max - self.min + 1)
            self.range = _range(series)
        else:
            counts = series.value_counts()
            self.distinct = len(counts)
            if self.distinct == 1 and not self.missing.any():
                self.type = "Constant"
            elif series.dtype == "bool" or self.distinct == 1 or self.distinct == 2:
                self.type = "Indicator"
            elif series.dtype == "O":
                self.type = "Categorical"
            else:
                self.type = "Continuous"
                self.range = _range(series)
