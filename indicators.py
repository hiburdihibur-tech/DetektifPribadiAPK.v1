import pandas as pd


def ema(close, period=20):
    close = pd.Series(close)
    return close.ewm(span=period, adjust=False).mean()


def macd(close):

    close = pd.Series(close)

    ema_fast = close.ewm(span=10, adjust=False).mean()
    ema_slow = close.ewm(span=20, adjust=False).mean()

    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=7, adjust=False).mean()

    return macd_line, signal_line


def volume_ma(volume, period=20):

    volume = pd.Series(volume)

    return volume.rolling(period).mean()


def macd_cross_up(macd, signal):

    return (
        macd.iloc[-3] <= signal.iloc[-3]
        and
        macd.iloc[-2] > signal.iloc[-2]
    )


def price_above_ema(close, ema20):

    return close[-1] > ema20.iloc[-1]


def volume_above_ma(volume, volume_ma20):

    return volume[-1] > volume_ma20.iloc[-1]


def signal_score(close, ema20, macd, signal, volume, volume_ma20):

    score = 0

    if macd_cross_up(macd, signal):
        score += 50

    if price_above_ema(close, ema20):
        score += 50

    return score