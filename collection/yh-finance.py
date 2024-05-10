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

    :param ticker:
    :param start_date:
    :return:
    """
    end_date = int(datetime.now().timestamp())

    # URL of the webpage containing the table
    url = (f'https://finance.yahoo.com/quote/{ticker}/history?period1={start_date}&period2={end_date}&interval=1d'
           f'&filter=history&frequency=1d')

    # Fetch the webpage
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    html = response.text

    if response.status_code != 200:
        raise RuntimeError('Invalid API Query (non-200 response value)')

    # Parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='svelte-ewueuo')

    # Extract the rows from the table
    rows = table.find_all('tr')

    # Initialize an empty list to store the data
    data = []

    # Loop over the rows
    for row in rows:
        # Extract the columns from each row
        cols = row.find_all('td')
        # If there are columns, extract the text and append to the data list
        if cols and len(cols) == 7:  # Avoid dividend rows
            data.append([ele.text.strip() for ele in cols])

    # Create a DataFrame using the extracted data
    # The first row will be used as the header
    return pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume'])


def date_to_unix(date_str):
    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date_str, '%b %d, %Y')

    # Convert the datetime object to Unix time
    # Subtract the epoch (Jan 1, 1970) from the date and get the total seconds
    unix_time = int((date_obj - datetime(1970, 1, 1)).total_seconds())

    return unix_time


if __name__ == '__main__':
    data = get_historical_data('SPY', date_to_unix('Mar 11, 2024'))
    print(data)