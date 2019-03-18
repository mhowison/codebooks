import pandas as pd

class Variable(object):

    def __init__(self, series):
        """
        """
        if not isinstance(series, pd.Series):
            raise ValueError("variable must be a pandas series object")

        self.name = series.name
        self.length = len(series)
        self.missing = series.isnull()

        # Determine variable type
        if series.is_unique:
            self.type = "Unique Key"
            self.distinct = self.length - self.missing.sum()
        else:
            self.counts = series.value_counts()
            self.distinct = len(self.counts)
            if self.distinct == 1:
                self.type = "Constant"
            elif series.dtype == "bool" or self.distinct == 2:
                self.type = "Indicator"
            elif series.dtype == "O":
                self.type = "Categorical"
            else:
                self.type = "Continuous"
                x = series.sort_values()
                n = self.length
                self.range = (x[0], x[int(0.25*n)], x[int(0.5*n)], x[int(0.75*n)], x[n-1])

