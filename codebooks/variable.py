import pandas as pd

class Variable(object):

    def __init__(self, series, desc=""):
        """
        """
        if not isinstance(series, pd.Series):
            raise ValueError("variable must be a pandas series object")

        self.name = series.name
        self.desc = desc
        self.missing = series.isnull()
        self.length = len(series)

        series = series[~self.missing]
        self.values = series.values
        self.values.sort()

        # Determine variable type
        if series.is_unique:
            self.type = "Unique Key"
            self.distinct = len(series)
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
                x = self.values
                n = len(x)
                self.range = (x[0], x[int(0.25*n)], x[int(0.5*n)], x[int(0.75*n)], x[n-1])

