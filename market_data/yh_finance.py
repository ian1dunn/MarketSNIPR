"""
yh-finance

A collection of web scraper utilities to obtain historical stock data from Yahoo Finance.



Author: Ian Dunn
"""
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_historical_data(ticker: str, start_date: int):
    """
    A function to query daily historical stock price data from Yahoo Finance. Includes date, open, high, low, close,
    adjusted close, and volume. Returns a pandas dataframe with the values from the given date to present.

    Converts timestamps to Unix

    :param ticker: The ticker symbol to query
    :param start_date: The start date of stock data in unix timestamp format
    :return:
    """
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
            data.append(_process_row([ele.text.strip() for ele in cols]))

    # Create a DataFrame using the extracted data
    # The first row will be used as the header
    return pd.DataFrame(data, columns=features)


def _process_row(columns):
    """
    Helper function to process the contents of a row of data given column values.

    1. Convert date to Unix timestamp

    :param columns: The values of the columns to process
    :return: The processed column values in list format
    """
    columns[0] = _date_to_unix(columns[0])
    return columns


def _date_to_unix(date_str):
    """
    Converts a date string in the format Mon dd, YYYY (ex. Mar 11, 2024) to Unix timestamp.

    :param date_str: The date string to return
    :return: The given date string in Unix timestamp format
    """
    date_obj = datetime.strptime(date_str, '%b %d, %Y')  # Convert date string to datetime object
    # Subtract epoch (Jan 1, 1970) from date and get the total seconds
    unix_time = int((date_obj - datetime(1970, 1, 1)).total_seconds())

    return unix_time


if __name__ == '__main__':
    data = get_historical_data('SPY', _date_to_unix('Mar 11, 2024'))
    print(data)