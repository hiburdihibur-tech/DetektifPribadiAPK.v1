import json
from datetime import datetime
from signal_state import already_sent, mark_sent, reset_symbol

from core.bybit import Bybit
from core.indicators import (
    ema,
    macd,
    volume_ma,
    macd_cross_up,
    price_above_ema,
    volume_above_ma,
    signal_score,
)

from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from core.telegram import TelegramBot

bot = TelegramBot(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)

BLACKLIST = {
    "XAUUSDT",
    "XAGUSDT",
    "SPYUSDT",
    "QQQUSDT",
    "NVDAUSDT",
    "MSFTUSDT",
    "METAUSDT",
    "AMDUSDT",
    "IBMUSDT",
    "SKHYNIXUSDT",
    "USDTUSD",
    "USDCUSDT",
    "FDUSDUSDT",
    "USD1USDT",
    "TUSDUSDT",
    "USDPUSDT",
    "RLUSDUSDT",
}

# ================================
# COIN LIST
# ================================

COIN_LIST_FILE = "data/coin_list.json"

def load_coin_list():
    try:
        with open(COIN_LIST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("❌ gagal membaca coin_list.json :", e)
        return[]


def scan(timeframe):

    print("=" * 60)
    print("DETEKTIF PRIBADI V2")
    print("by HENDY CHINTO")
    print("=" * 60)

    print("mengambil data...")

    api = Bybit()

    print("Memuat Watchlist...!")

    df = load_coin_list()

    hasil = []
    total = len(df)
    current = 0

    for symbol in df:
        current += 1
        print(f"\rScanning {current}/{total} | Signal: {len(hasil):2}", end="", flush=True,)

    

        if symbol in BLACKLIST:
            continue

        try:
            
            close, volume = api.get_klines(symbol, timeframe)

            if close is None:
                continue

            #===== DEBUG BTCUSDT =====
            if symbol == "BTCUSDT":
                print("\n========== DEBUG BTCUSDT ==========")
                print(f"Jumlah Candle : {len(close)}")
                print("5 Close Terakhir :")

                for i in range(-5, 0):
                    print(f"{i} : {close[i]}")

                print("==================================\n")
                # ========================

                


            print(f"TIMEFRAME AKTIF : {timeframe}")
            
            if close is None:
                continue

            ema20 = ema(close)

            macd_line, signal = macd(close)
            print(f"\n{symbol}")
            print(f"MACD -2 : {macd_line.iloc[-2]:.8f}")
            print(f"SIG  -2 : {signal.iloc[-2]:.8f}")
            print(f"MACD -1 : {macd_line.iloc[-1]:.8f}")
            print(f"SIG  -1 : {signal.iloc[-1]:.8f}")
            cross =(
                macd_line.iloc[-2] <= signal.iloc[-2]
                and
                macd_line.iloc[-1] > signal.iloc[-1]
            )
            print(f"GOLDEN CROSS : {cross}")
            print("--------------------")

            volume20 = volume_ma(volume)

            print(symbol,
                  "Price:", close[-1],
                  "EMA20:", ema20.iloc[-1],
                  "MACD:", macd_line.iloc[-1],
                  "Signal:", signal.iloc[-1]
                  )
            
            if not price_above_ema(close, ema20):
                continue

            golden = macd_cross_up(macd_line, signal)

            if golden:
                status = "STRONG SIGNAL"
            else:
                status = "EARLY SIGNAL"
                 

            

    
            
            score = signal_score(
            close,
            ema20,
            macd_line,
            signal,
            volume,
            volume20,
            )
            print(f">>> BUY SIGNAL {symbol}")
            hasil.append({
                "symbol": symbol,
                "score": score,
                "close": close[-1],
                "ema20": float(ema20.iloc[-1]),
                "macd": float(macd_line.iloc[-1]),
                "signal": float(signal.iloc[-1]),
                "volume": volume[-1],
                "volume_ma20": float(volume20.iloc[-1]),
            })

            if status == "STRONG SIGNAL":
                title ="🟢 STRONG SIGNAL"
            else:
                title = "🟡 EARLY SIGNAL"
           

        
            
        

            message = f"""
            🚀 {title}

            Coin : {symbol}
            ⭐ Score : {score:.1f}/100

            Price : {close[-1]:.6f}
            EMA20 : {float(ema20.iloc[-1]):.6f}
            MACD : {float(macd_line.iloc[-1]):.6f}
            Signal : {float(signal.iloc[-1]):.6f}

            Volume : {volume[-1]:.2f}
            Volume MA20 : {float(volume20.iloc[-1]):.2f}
            """
        
            if not already_sent(symbol):
                bot.send(message, symbol)
                mark_sent(symbol)
        
        except Exception as e:
            print(f"gagal : {e}")
            continue


    hasil = sorted(hasil, key=lambda x: x["score"], reverse=True)
    
    print()
    print("=" * 60)
    print("TOTAL SIGNAL :", len(hasil))
    print("=" * 60)

    for i, coin in enumerate(hasil, start=1):

     print()

     print(f"{i}. {coin['symbol']}")

     star = "⭐" * min(5, max(1, int(coin["score"] / 20)))
    
     print(f"Rating       : {star}")
     print(f"Score        : {coin['score']:.1f}/100")
     print(f"Close        : {coin['close']:.6f}")
     print(f"EMA20        : {coin['ema20']:.6f}")
     print(f"MACD         : {coin['macd']:.6f}")
     print(f"Signal       : {coin['signal']:.6f}")
     print(f"Volume       : {coin['volume']:.2f}")
     print(f"Volume MA20  : {coin['volume_ma20']:.2f}")

    print()
    print("=" * 60)
    print("SCAN SELESAI")
    print("=" * 60)

    try:
        with open("data/scan_history.json", "w", encoding="utf-8") as f:
            json.dump(
    {
        "scan_time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "results": hasil
    },
    f,
    indent=4,
    ensure_ascii=False
)
            print("✅ scan_history.json berhasil disimpan")

    except Exception as e:
        print("❌ Gagal menyimpan scan_history :", e)

    return hasil