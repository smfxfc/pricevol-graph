#! python3
"""Pull trading data from Cryptocompare and graph trailing 3-month price/volume activity"""

from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import requests

from pprint import pprint


# retrieve dataframe
def retrieve_data(
    symbol, comparison_symbol="USD", limit=1, aggregate=1, allData="true"
):
    """Note that raw dataframe includes empty data rows for periods where the token didn't exist. Not an issue for graphing trailing 3-months, but will skew metric calculations for full period."""
    url = f"https://min-api.cryptocompare.com/data/histoday?fsym={symbol}&tsym={comparison_symbol}&limit={limit}&aggregate={aggregate}&allData={allData}&tryconversion=true"
    page = requests.get(url)
    data = page.json()["Data"]
    df = pd.DataFrame(data)
    return df


def format_data(df):
    """
    Strip dataframe to required columns and format times from unix to m/d/Y.
    TODO: is this even necessary?
    """
    df["time"] = [datetime.fromtimestamp(d) for d in df.time]
    df["time"] = df["time"] + pd.Timedelta(
        hours=12
    )  # toggle this depending on timezone.
    df["time"] = pd.to_datetime(df.time)

    df["time"] = df["time"].dt.strftime("%m/%d/%Y")
    return df
