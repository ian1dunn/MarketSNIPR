"""
yh-finance

A collection of web scraper utilities to obtain historical stock data from Yahoo Finance.



Author: Ian Dunn
"""
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_historical_data(ticker: str, start_date: datetime, save_csv=False) -> pd.DataFrame:
    """
    A function to query daily historical stock price data from Yahoo Finance. Includes date, open, high, low, close,
    adjusted close, and volume. Returns a pandas dataframe with the values from the given date to present.

    Converts timestamps to Unix

    :param ticker: The ticker symbol to query
    :param start_date: The start date of stock data with date strings replaced by datetime objects
    :return:
    """
    start_date = int(start_date.timestamp())
    end_date = int(datetime.now().timestamp())
    features = ['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']
    url = (f'https://finance.yahoo.com/quote/{ticker}/history?period1={start_date}&period2={end_date}&interval=1d'
           f'&filter=history&frequency=1d')

    # Fetch webpage
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    html = response.text

    if response.status_code != 200:
        raise RuntimeError('Invalid API Query (non-200 response value)')

    # Parse HTML content
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='svelte-ewueuo')

    # Extract rows from the table
    rows = table.find_all('tr')
    data = []
    for row in rows:
        # Extract the columns from each row
        cols = row.find_all('td')
        # If there are columns, extract the text and append to the data list
        if cols and len(cols) == len(features):  # Avoid dividend rows
            col_names = [ele.text.strip() for ele in cols]
            col_names[0] = date_to_datetime(col_names[0])  # Convert date to datetime
            col_names[6] = int(col_names[6].replace(',', ''))  # Convert volume to int
            data.append(col_names)

    df = pd.DataFrame(data, columns=features)
    df = df.iloc[::-1].reset_index(drop=True)  # Reverse final dataframe so dates are in chronological order

    if save_csv:
        os.makedirs('./csv', exist_ok=True)
        df.to_csv(f'./csv/yh_finance_data_{ticker}.csv', index=False)

    return df


def date_to_datetime(date_str: str) -> datetime:
    """
    Converts a date string in the format Mon dd, YYYY (ex. Mar 11, 2024) to Unix timestamp.

    :param date_str: The date string to convert to Unix timestamp
    :return: The Unix timestamp of the given string
    """
    return datetime.strptime(date_str, '%b %d, %Y')  # Convert date string to datetime object
    # unix_time = int((date_obj - datetime(1970, 1, 1)).total_seconds())


if __name__ == '__main__':
    data = get_historical_data('MSFT', datetime(2024, 3, 11), save_csv=True)
    print(data)
