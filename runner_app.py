import time
from scanner import scan


def start_scanner(
        timeframe="15", 
        stop_event=None,
        scan_interval =60,
):

    print(f"🚀 Scanner APK Dimulai | TF = {timeframe} | Interval = {scan_interval}")

    while True:

        if stop_event and stop_event.is_set():
            print("🛑 Scanner dihentikan")
            break

        scan(timeframe)

        for _ in range(scan_interval):

            if stop_event and stop_event.is_set():
                print("🛑 Scanner dihentikan")
                return

            time.sleep(1)