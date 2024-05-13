import pandas as pd
from ta.momentum import RSIIndicator, StochasticOscillator, ROCIndicator, WilliamsRIndicator
from ta.trend import MACD, SMAIndicator, EMAIndicator
from ta.volume import AccDistIndexIndicator, OnBalanceVolumeIndicator

import config


def add_technical_indicators(df: pd.DataFrame, window: int = config.LOOK_BACK_WINDOW) -> pd.DataFrame:
    """
    Adds ten most famous indicators used by technical traders to the DataFrame:
    ADI, OBV, RSI, SR, ROC, WR, MACD, EMA, SMA, Disparity Index

    Parameters:
    df (pd.DataFrame): DataFrame containing columns ['open', 'high', 'low', 'close', 'volume'].
    window (int): Look-back window period for indicators.

    Returns:
    pd.DataFrame: DataFrame with additional columns for each technical indicator.
    """
    indicators = _build_indicator_classes(df, window)

    # Accumulation/Distribution Index (ADI)
    df['adi'] = indicators['adi'].acc_dist_index()

    # On-Balance Volume (OBV)
    df['obv'] = indicators['obv'].on_balance_volume()

    # Relative Strength Index (RSI)
    df['rsi'] = indicators['rsi'].rsi()

    # Stochastic Oscillator (SR)
    df['sr'] = indicators['sr'].stoch()

    # Rate of Change (ROC)
    df['roc'] = indicators['roc'].roc()

    # Williams %R (WR)
    df['wr'] = indicators['wr'].williams_r()

    # Moving Average Convergence Divergence (MACD)
    df['macd'] = indicators['macd'].macd()

    # Exponential Moving Average (EMA)
    df['ema'] = indicators['ema'].ema_indicator()

    # Simple Moving Average (SMA)
    df['sma'] = indicators['sma'].sma_indicator()

    df['disp_index'] = (df['close'] / df['ema']) * 100

    return df


def _build_indicator_classes(df: pd.DataFrame, window: int) -> dict:
    return {
        'adi': AccDistIndexIndicator(high=df['high'], low=df['low'], close=df['close'], volume=df['volume'],
                                     fillna=True),
        'obv': OnBalanceVolumeIndicator(close=df['close'], volume=df['volume'], fillna=True),
        'rsi': RSIIndicator(close=df['close'], window=window, fillna=True),

        # TODO smooth window
        'sr': StochasticOscillator(high=df['high'], low=df['low'], close=df['close'], window=window, fillna=True),
        'roc': ROCIndicator(close=df['close'], window=window, fillna=True),
        'wr': WilliamsRIndicator(high=df['high'], low=df['low'], close=df['close'], lbp=window, fillna=True),

        # TODO different windows
        'macd': MACD(close=df['close'], fillna=True),
        'ema': EMAIndicator(close=df['close'], window=window, fillna=True),
        'sma': SMAIndicator(close=df['close'], window=window, fillna=True)
    }
