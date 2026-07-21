import requests

class Bybit:

    BASE_URL = "https://api.binance.com"

    def __init__(self):
        self.session = requests.Session()

    def get_klines(self, symbol, interval="15", limit=100):

        interval_map = {
            "1": "1m",
            "5": "5m",
            "15": "15m",
            "30": "30m",
            "60": "1h",
            "240": "4h",
            "D": "1d",
        }

        interval = interval_map.get(str(interval), str(interval))

        url = f"{self.BASE_URL}/api/v3/klines"

        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
        }

        try:
            r = self.session.get(
                url,
                params=params,
                timeout=10,
            )

            r.raise_for_status()

            data = r.json()

            if not data:
                return None, None

            close = [float(x[4]) for x in data]
            volume = [float(x[5]) for x in data]

            return close, volume

        except Exception as e:
            print(f"{symbol} ERROR : {e}")
            return None, None

    def get_symbols(self):

        url = f"{self.BASE_URL}/api/v3/exchangeInfo"

        r = self.session.get(url, timeout=30)
        r.raise_for_status()

        data = r.json()

        symbols = []

        for s in data["symbols"]:

            if (
                s["status"] == "TRADING"
                and s["quoteAsset"] == "USDT"
                and s["isSpotTradingAllowed"]
            ):
                symbols.append(s["symbol"])

        return symbols

    def get_top_gainers(self):

        url = f"{self.BASE_URL}/api/v3/ticker/24hr"

        r = self.session.get(url, timeout=30)
        r.raise_for_status()

        data = r.json()

        coins = [
            x for x in data
            if x["symbol"].endswith("USDT")
        ]

        coins.sort(
            key=lambda x: float(x["priceChangePercent"]),
            reverse=True
        )

        return coins


if __name__ == "__main__":

    api = Bybit()

    print(f"Total Pair : {len(api.get_symbols())}")