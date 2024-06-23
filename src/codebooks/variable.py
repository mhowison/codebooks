"""
Class for representing a variable and inferring its type.
"""

from numpy import sort
from pandas import Series


class Variable(object):

    def __init__(self, series: Series, desc: str = ""):
        """
        """
        self.name = series.name
        self.desc = desc
        self.missing = series.isnull()
        self.length = len(series)

        series = series[~self.missing]
        self.values = sort(series.values)

        # Determine variable type
        if series.is_unique:
            if len(series) == 0:
                self.type = "Empty"
            else:
                self.type = "Unique Key"
            self.distinct = len(series)
        else:
            self.counts = series.value_counts()
            self.distinct = len(self.counts)
            if self.distinct == 1:
                self.type = "Constant"
            elif series.dtype == "bool" or self.distinct == 2:
                self.type = "Indicator"
            elif series.dtype == "O" or series.dtype == "category" or self.distinct <= 10:
                self.type = "Categorical"
            else:
                self.type = "Numeric"
                x = self.values
                n = len(x)
                self.range = (
                    x[0],
                    x[int(0.25 * n)],
                    x[int(0.50 * n)],
                    x[int(0.75 * n)],
                    x[n - 1]
                )
