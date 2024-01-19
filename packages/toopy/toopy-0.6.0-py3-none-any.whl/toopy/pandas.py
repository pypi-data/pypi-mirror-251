import pandas as pd
import itertools as it

def read_csv_list(filenames, kwargs={}):
    dfs = []
    for filename in filenames:
        try:
            dfs.append(pd.read_csv(filename, **kwargs))
        except UnicodeDecodeError:
            raise UnicodeDecodeError(f"{filename} contained invalid start byte. Try saving it with utf-8 encoding.")
    return pd.concat(dfs)

def expand_grid(data_dict):
    """Create a dataframe from every combination of given values."""
    rows = it.product(*data_dict.values())
    return pd.DataFrame.from_records(rows, columns=data_dict.keys())

def flatten_columns_and_replace(df, search=None, replace=None):
    collist = [a+b for a, b in list(df.columns.to_flat_index())]
    collist = [colname.replace(search, replace) for colname in collist]
    df.columns = collist
    return df