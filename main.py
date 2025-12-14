import telebot
import requests
import time
import threading
from flask import Flask
import os

# توکن تلگرام
TOKEN = "1073308116:AAH0mweKwZDPjep9bXq9AQ0Sa6psaP4Q9_k"
CHAT_ID = "@praiceday"

bot = telebot.TeleBot(TOKEN)
app = Flask(name)

# آدرس API جدید
API_CRYPTO = "https://candobots.ir/api/arzlive-api.php?currency=usdt,btc,ton,not,paxg"

def get_prices():
    try:
        data = requests.get(API_CRYPTO, timeout=10).json()
        print("API Response:", data)  # لاگ برای Railway

        msg = (
            f"💰 کریپتو:\n"
            f"🇺🇸 تتر (USDT): {data.get('usdt', {}).get('price', 'ناموجود'):,}\n"
            f"💰 بیت کوین (BTC): {data.get('btc', {}).get('price', 'ناموجود'):,}\n"
            f"💎 تون کوین (TON): {data.get('ton', {}).get('price', 'ناموجود'):,}\n"
            f"🎮 نات کوین (NOT): {data.get('not', {}).get('price', 'ناموجود'):,}\n"
            f"🟡 گلد (PAXG): {data.get('paxg', {}).get('price', 'ناموجود'):,}\n\n"
            f"📮 {data.get('usdt', {}).get('updated_at', '')}\n"
            f"#کریپتو #بیتکوین #تتر #TON #NOT #PAXG"
        )
        return msg
    except Exception as e:
        print("API Error:", e)
        return f"⚠️ خطا در API: {e}"

def auto_send():
    while True:
        bot.send_message(CHAT_ID, get_prices())
        time.sleep(300)  # هر ۱۰ دقیقه

threading.Thread(target=auto_send, daemon=True).start()

@app.route("/")
def home():
    return "Bot Running Successfully"

if name == "main":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)            f"🟡 سکه امامی: {golds.get('seke', {}).get('price', 0):,}\n"
            f"🟡 تمام سکه: {golds.get('tamam', {}).get('price', 0):,}\n"
            f"🟡 نیم سکه: {golds.get('nim', {}).get('price', 0):,}\n"
            f"🟡 ربع سکه: {golds.get('rob', {}).get('price', 0):,}\n"
            f"🟡 گرم طلا: {golds.get('geram18', {}).get('price', 0):,}\n"
            f"🟡 مثقال طلا: {golds.get('mesghal', {}).get('price', 0):,}\n"
            f"🟡 انس طلا: $ {golds.get('ounce', {}).get('price', 0):,}\n\n"

            f"💰 بیت کوین: $ {crypto.get('bitcoin', {}).get('sell', 0):,}\n\n"

            f"📮 {updated}\n"
            f"#طلا #دلار #بیتکوین #سکه"
        )
        return msg
    except Exception as e:
        print("API Error:", e)
        return f"⚠️ خطا در API: {e}"

def auto_send():
    while True:
        bot.send_message(CHAT_ID, get_prices())
        time.sleep(300)  # هر ۱۰ دقیقه

threading.Thread(target=auto_send, daemon=True).start()

@app.route("/")
def home():
    return "Bot Running Successfully"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
