from datetime import datetime

import exchange_calendars as xcals
import pandas as pd

from market_data.indicators import add_technical_indicators


def preprocess(df: pd.DataFrame):
    # Remove timestamps that do not correspond with open market days
    # Note: not necessary when using yahoo finance, but would be useful for removing weekend/holiday sentiment analysis
    open_dates = _get_open_dates(df.iloc[0].date, df.iloc[-1].date)
    df.drop(df[df.date != open_dates].index, inplace=True)

    # Remove adj_close
    df.drop(columns=['adj_close'], inplace=True)

    # Compute technical indicators
    df_indicators = add_technical_indicators(df)

    # Remove open, low, high, and volume
    df_indicators.drop(columns=['open', 'low', 'high', 'volume'], inplace=True)

    # TODO normalize data points so all stocks have equal length
    #  or, entirely remove dates and say stocks must have >X year previous history to be included in the portfolio?
    """
    "Further dataset processing is required to ensure that all financial assets (stocks) considered in the portfolio 
    have an equal length of historical data points. Some stocks have been recorded for decades, while other newly 
    listed stocks are only a few months. This time-dimension alignment of stocks’ historical data will prevent the 
    biased action of the agent toward the stock with more data."
    """

    # TODO regularize all columns except date by normalizing the observation space using Batch Normalization

    return df_indicators


def _get_open_dates(start_date: datetime, end_date: datetime):
    xnys = xcals.get_calendar("XNYS")  # New York Stock Exchange
    return xnys.sessions_in_range(str(start_date), str(end_date))


if __name__ == "__main__":
    df = pd.read_csv("./csv/yh_finance_data_MSFT.csv", parse_dates=['date'])
    print(preprocess(df).info())
