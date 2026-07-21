import requests

class TelegramBot:

    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def send(self, message, symbol=None):

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        data = {
            "chat_id": self.chat_id,
            "text": message,
        }

        # Tambahkan tombol BINANCE jika symbol ada
        if symbol:
            data["reply_markup"] = {
                "inline_keyboard": [[
                    {
                        "text": "🔍 CEK SEKARANG",
                        "url": f"https://www.binance.com/en/trade/{symbol.replace('USDT','_USDT')}"
                    }
                ]]
            }

        response = requests.post(
            url,
            json=data,
            timeout=30,
        )

        print(response.status_code)
        print(response.text)