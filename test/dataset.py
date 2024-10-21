import numpy as np
import pandas as pd

N = 1000000

np.random.seed(1230402)

data = pd.DataFrame(
    index=pd.Index(np.arange(N), name="id"),
    data={
        "date": np.datetime64("2020-01-01") + np.random.randint(0, 1000, size=N),
        "bool": np.random.choice([0,1], size=N),
        "categorical": np.random.choice(["A", "B", "C", "D", "E"], size=N),
        "pandas_categorical": pd.Categorical(np.random.choice(["A", "B", "C", "D", "E"], size=N)),
        "numerical_categorical": np.random.choice(range(0, 10), size=N),
        "ordered_categorical": pd.Categorical(np.random.choice(range(0, 10), size=N), ordered=True),
        "numerical": np.round(np.random.randn(N), decimals=2)
    }
)

data.to_csv("dataset.csv")
data.to_parquet("dataset.parquet")
