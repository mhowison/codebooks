"""
Class for representing a variable and inferring its type.
"""

from numpy import datetime_as_string, sort
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
            elif series.dtype == "category" and series.dtype.ordered == True:
                self.type = "Ordered Categorical"
            elif series.dtype == "O" or series.dtype == "category" or self.distinct <= 10:
                self.type = "Categorical"
            elif hasattr(series, "dt"):
                self.type = "Date"
                self.range = list(map(
                    lambda x: datetime_as_string(x, unit="D"),
                    series.quantile([0, 0.25, 0.5, 0.75, 1]).values
                ))
            else:
                self.type = "Numeric"
                self.range = series.quantile([0, 0.25, 0.5, 0.75, 1]).tolist()
