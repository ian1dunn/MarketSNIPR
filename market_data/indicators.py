from config import LOOK_BACK_WINDOW


def rsi(df, W=LOOK_BACK_WINDOW):
    """
    Compute the Relative Strength Index (RSI) for a given DataFrame.

    :param: dataframe: A DataFrame with columns 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume'.
    :param: W: The lookback period for calculating the RSI.

    :return: Original DataFrame with an additional 'RSI' column.
    """
    df = df.copy()
    # Calculate price differences
    delta = df['adj_close'].diff()

    # Make two series: one for gains and the other for losses
    gain = (delta.where(delta > 0, 0))
    loss = (-delta.where(delta < 0, 0))

    # Calculate the exponential moving average of gains and losses
    avg_gain = gain.ewm(com=W - 1, min_periods=W).mean()
    avg_loss = loss.ewm(com=W - 1, min_periods=W).mean()

    # Calculate the RSI
    RS = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + RS))

    # Handle cases where there is no price change (avoid division by zero)
    df['RSI'] = df['RSI'].fillna(50)  # where avg_gain and avg_loss are both 0, RS is considered as 1 (50% RSI)

    return df


def sma(df, W=LOOK_BACK_WINDOW):
    """
    Simple Moving Average (SMA): An important indicator to identify current price trends and the potential for a change
    in an established trend. Computes the closing price SMA for a given DataFrame.

    :param: dataframe: A DataFrame with columns 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume'.
    :param: W: The lookback period for calculating the SMA.

    :return: Original DataFrame with an additional column for the SMA.
    """
    df = df.copy()
    df[f'SMA'] = df["close"].rolling(window=W).mean()
    return df


def ema(df, W=LOOK_BACK_WINDOW):
    """
    Exponential Moving Average (EMA): Like SMA, EMA is a technical indicator used to spot current trends over time.
    However, EMA is considered an improved version of SMA by giving more weight to the recent prices considering old
    price history less relevant; therefore it responds more quickly to price changes than SMA. Computes the closing
    price EMA for a given DataFrame.

    :param: dataframe: A DataFrame with columns 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume'.
    :param: W: The lookback period for calculating the EMA.

    :return: Original DataFrame with an additional column for the EMA.
    """
    df = df.copy()
    df[f'EMA'] = df['close'].ewm(span=W, adjust=False).mean()
    return df


def stochastic_osc(df, W=LOOK_BACK_WINDOW, smooth_k=3, smooth_d=3):
    """
    Stochastic Oscillator (%K): A momentum indicator comparing the closing price of the stock to a range of its prices
    in a look-back window period W. Computes this for a given DataFrame.

    :param: dataframe: A DataFrame with columns 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume'.
    :param: W: The lookback period for calculating the %K.
    :param: smooth_k: The smoothing factor for %K line.
    :param: smooth_d: The smoothing factor for %D line, which is the moving average of the %K.

    :return: Original DataFrame with an additional column for the %K.
    """
    df = df.copy()
    # Calculate the rolling high and low
    low_min = df['low'].rolling(window=W).min()
    high_max = df['high'].rolling(window=W).max()

    # Calculate %K line
    df['%K'] = ((df['close'] - low_min) / (high_max - low_min) * 100)
    # Smoothing %K line
    df['%K'] = df['%K'].rolling(window=smooth_k).mean()

    # Calculate %D line (SMA of %K line)
    # df['%D'] = df['%K'].rolling(window=smooth_d).mean() TODO

    return df


def macd(df, W=LOOK_BACK_WINDOW, slow=26, fast=12):
    """
    Moving Average Convergence/Divergence (MACD): Is one of the most used momentum indicators to identify the
    relationship between two moving averages of the stock price and it helps the agent to understand whether the
    bullish or bearish movement in the price is strengthening or weakening. Compute this for a given DataFrame.

    :param: dataframe: A DataFrame with columns 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume'.
    :param: W: The lookback period for calculating the MACD.

    :return: Original DataFrame with an additional column for the MACD.
    """

    df = df.copy()
    # Calculate the fast and slow EMAs
    df['EMA_fast'] = df['close'].ewm(span=fast, adjust=False).mean()
    df['EMA_slow'] = df['close'].ewm(span=slow, adjust=False).mean()

    # Calculate the MACD
    df['MACD'] = df['EMA_fast'] - df['EMA_slow']

    # Calculate the Signal line
    # df['Signal_line'] = df['MACD'].ewm(span=signal, adjust=False).mean()

    return df


def a_d(df, W=LOOK_BACK_WINDOW):
    """
    Accumulation/Distribution Oscillator: A volume-based cumulative momentum indicator that helps the agent to assess
    whether the stock is being accumulated (bought) or distributed (sold) by measuring the divergences between the
    volume flow and the stock price.

    :return:
    """
    pass


def obv(df, W=LOOK_BACK_WINDOW):
    """
    On-Balance Volume Indicator (OBV): Another volume-based momentum indicator that uses volume flow to predict the
    changes in stock price

    :return:
    """
    pass


def roc(df, W=LOOK_BACK_WINDOW):
    """
    Price Rate Of Change (ROC): A momentum-based indicator that measures the speed of stock price changes over the
    look-back window W.

    :return:
    """
    pass


def williams(df, W=LOOK_BACK_WINDOW):
    """
    William’s %R: Known also as Williams Percent Range, is a momentum indicator used to spot entry and exit points in
    the market by comparing the closing price of the stock to the high-low range of prices in the look-back window (W).

    :return:
    """
    pass


def disp_index(df, W=LOOK_BACK_WINDOW):
    """
    Disparity Index: A percentage that indicates the relative position of the current closing price of the stock to a
    selected moving average. In this study, the selected moving average is the EMA of the look-back window (W).

    :return:
    """
    pass
