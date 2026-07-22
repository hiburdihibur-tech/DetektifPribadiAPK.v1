from typing import List


def ema(close: List[float], period=20):

    if not close:
        return []

    alpha = 2 / (period + 1)

    result = [float(close[0])]

    for price in close[1:]:
        result.append(alpha * float(price) + (1 - alpha) * result[-1])

    return result


def macd(close):

    ema_fast = ema(close, 10)
    ema_slow = ema(close, 20)

    macd_line = []

    for f, s in zip(ema_fast, ema_slow):
        macd_line.append(f - s)

    signal_line = ema(macd_line, 7)

    return macd_line, signal_line


def volume_ma(volume, period=20):

    result = []

    for i in range(len(volume)):
        if i + 1 < period:
            result.append(None)
        else:
            window = volume[i - period + 1:i + 1]
            result.append(sum(window) / period)

    return result


def macd_cross_up(macd, signal):

    if len(macd) < 3 or len(signal) < 3:
        return False

    return (
        macd[-3] <= signal[-3]
        and
        macd[-2] > signal[-2]
    )


def price_above_ema(close, ema20):

    return close[-1] > ema20[-1]


def volume_above_ma(volume, volume_ma20):

    if volume_ma20[-1] is None:
        return False

    return volume[-1] > volume_ma20[-1]


def signal_score(close, ema20, macd, signal, volume, volume_ma20):

    score = 0

    if macd_cross_up(macd, signal):
        score += 50

    if price_above_ema(close, ema20):
        score += 50

    return score
