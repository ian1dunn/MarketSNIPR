import pandas as pd
import ta

import config


def add_technical_indicators(df: pd.DataFrame, window: int = config.LOOK_BACK_WINDOW) -> pd.DataFrame:
    """
    Adds technical indicators to the DataFrame.

    Parameters:
    df (pd.DataFrame): DataFrame with columns ['open', 'high', 'low', 'close', 'volume'].
    window (int): Look-back window period for indicators.

    Returns:
    pd.DataFrame: DataFrame with additional columns for each technical indicator.
    """
    df['RSI'] = ta.momentum.rsi(df['close'], window=window)
    df['SMA'] = df['close'].rolling(window=window).mean()
    df['EMA'] = df['close'].ewm(span=window, adjust=False).mean()
    df['Stochastic_%K'] = ta.momentum.stoch(df['high'], df['low'], df['close'], window=window)
    df['MACD'] = ta.trend.macd(df['close'])
    df['A/D'] = ta.volume.acc_dist_index(df['high'], df['low'], df['close'], df['volume'])
    df['OBV'] = ta.volume.on_balance_volume(df['close'], df['volume'])
    df['ROC'] = ta.momentum.roc(df['close'], window=window)
    df['Williams_%R'] = ta.momentum.williams_r(df['high'], df['low'], df['close'], lbp=window)
    df['Disparity_Index'] = (df['close'] / df['EMA']) * 100

    return df