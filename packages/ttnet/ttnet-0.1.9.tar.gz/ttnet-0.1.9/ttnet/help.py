import pandas as pd


def df(d: dict) -> pd.DataFrame:
    return pd.DataFrame.from_dict(d)
