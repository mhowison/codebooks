import pandas as pd
from collections import Counter
from timeit import timeit

print(
    "pandas read_csv:",
    timeit(
        'pd.read_csv("dataset.csv")',
        setup='import pandas as pd',
        number=10
    )
)

print(
    "pandas read_csv dtype=str:",
    timeit(
        'pd.read_csv("dataset.csv", dtype=str)',
        setup='import pandas as pd',
        number=10
    )
)

df = pd.read_csv("dataset.csv")

for col in df.columns:
    print(col)
    print(
        "  pandas value_counts:",
        timeit(
            'df[col].value_counts()',
            globals={"df": df, "col": col},
            number=10
        )
    )
    print("  Counter:",
        timeit(
            'Counter(df[col])',
            globals={"df": df, "col": col, "Counter": Counter},
            number=10
        )
    )
