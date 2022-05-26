#! python3
"""Pull trading data from Cryptocompare and graph trailing 3-month price/volume activity"""

# TODO: take symbol input from user

from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import requests

from plotly.subplots import make_subplots
import plotly.graph_objects as go
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
        hours=0
    )  # toggle this depending on timezone.
    df["time"] = pd.to_datetime(df.time)
    df["time"] = df["time"].dt.strftime("%m/%d/%Y")
    return df


df = retrieve_data("ETH")
df = format_data(df)
graph_df = df.tail(90)  # only plotting last 90 days


# set up plotly figure
fig = make_subplots(1, 2)

# add first scatter trace at row = 1, col = 1
fig.add_trace(
    go.Scatter(
        x=graph_df["time"],
        y=graph_df["close"],
        line=dict(color="blue"),
        name="Closing Price",
        showlegend=True,
    )
)
fig.update_layout(
    yaxis=dict(tickprefix="$", tickformat=","),
    xaxis=dict(dtick=4, tickangle=-45),
    legend=dict(
        orientation="h",
        x=0.2,
        traceorder="normal",
        font=dict(family="Calibri", size=12, color="Blue"),
    ),
)

# TODO: add secondary y axis and bar chart of volume data
# fig.update_yaxes(title_text="Column1", secondary_y=True)

fig.show()
