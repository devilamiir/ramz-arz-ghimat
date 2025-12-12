import telebot
import requests
import time
import threading
from flask import Flask
import os

TOKEN = "1073308116:AAH0mweKwZDPjep9bXq9AQ0Sa6psaP4Q9_k"
CHAT_ID = 714402925

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

API_URL = "https://varzesh3-api.vercel.app/api/prices"

def get_prices():
    try:
        r = requests.get(API_URL, timeout=10).json()

        msg = (
            f"🇺🇸 دلار آزاد: {r['dollar_free']}\n"
            f"🇺🇸 صرافی ملی: {r['dollar_national']}\n"
            f"🇪🇺 یورو: {r['euro']}\n"
            f"🇬🇧 پوند: {r['pound']}\n"
            f"🇹🇷 لیر ترکیه: {r['lira']}\n\n"
            f"🟡 سکه امامی: {r['seke']}\n"
            f"🟡 نیم سکه: {r['nim']}\n"
            f"🟡 ربع سکه: {r['rob']}\n"
            f"🟡 گرم طلا: {r['geram18']}\n"
            f"🟡 مثقال: {r['mesghal']}\n"
            f"🟡 انس طلا: $ {r['ounce']}\n\n"
            f"💰 تتر: {r['tether']}\n"
            f"💰 بیت‌کوین: $ {r['bitcoin']}\n\n"
            f"⏱ آپدیت هر ۱۰ دقیقه"
        )

        return msg
    except Exception as e:
        return f"⚠️ خطا در API: {e}"


def auto_send():
    while True:
        bot.send_message(CHAT_ID, get_prices())
        time.sleep(600)  # 10 دقیقه


threading.Thread(target=auto_send, daemon=True).start()


@app.route("/")
def home():
    return "Bot Running Successfully"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# اجرای ترد
threading.Thread(target=auto_send, daemon=True).start()


# -----------------------------
# Railway
# -----------------------------
@app.route("/")
def home():
    return "Bot Running OK."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
