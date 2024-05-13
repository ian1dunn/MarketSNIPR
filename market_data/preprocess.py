from datetime import datetime

import exchange_calendars as xcals
import pandas as pd

from market_data.indicators import rsi


def preprocess(df: pd.DataFrame):
    # Remove timestamps that do not correspond with open market days
    open_dates = _get_open_dates(df.iloc[0].date, df.iloc[-1].date)
    df.drop(df[df.date != open_dates].index, inplace=True)

    # Ensure equal length of historical data points to avoid bias

    # TODO Compute statistics
    df = rsi(df)

    # Remove adj_close and volume

    return df


def _get_open_dates(start_date: datetime, end_date: datetime):
    xnys = xcals.get_calendar("XNYS")  # New York Stock Exchange
    return xnys.sessions_in_range(str(start_date), str(end_date))


if __name__ == "__main__":
    df = pd.read_csv("./csv/yh_finance_data_MSFT.csv", parse_dates=['date'])
    print(preprocess(df))
