import telebot
import requests
import time
import threading
from flask import Flask
import os

# توکن تلگرام
TOKEN = "1073308116:AAH0mweKwZDPjep9bXq9AQ0Sa6psaP4Q9_k"
CHAT_ID = 714402925

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# آدرس‌های API جدید
API_CURRENCIES = "https://api.alanchand.com/?type=currencies&token=AdVB8dhKJQJ0jGaBKHhe"
API_GOLDS = "https://api.alanchand.com/?type=golds&token=AdVB8dhKJQJ0jGaBKHhe"
API_CRYPTO = "https://api.alanchand.com/?type=crypto&token=AdVB8dhKJQJ0jGaBKHhe"

def get_prices():
    try:
        # گرفتن داده‌ها
        currencies = requests.get(API_CURRENCIES, timeout=10).json()
        golds = requests.get(API_GOLDS, timeout=10).json()
        crypto = requests.get(API_CRYPTO, timeout=10).json()

        # ساخت پیام
        msg = (
            f"💵 ارزها:\n"
            f"🇺🇸 دلار آزاد: {currencies.get('usd', 'ناموجود')}\n"
            f"🇪🇺 یورو: {currencies.get('eur', 'ناموجود')}\n"
            f"🇬🇧 پوند: {currencies.get('gbp', 'ناموجود')}\n"
            f"🇹🇷 لیر ترکیه: {currencies.get('try', 'ناموجود')}\n\n"
            
            f"🟡 طلا و سکه:\n"
            f"سکه امامی: {golds.get('seke', 'ناموجود')}\n"
            f"نیم سکه: {golds.get('nim', 'ناموجود')}\n"
            f"ربع سکه: {golds.get('rob', 'ناموجود')}\n"
            f"گرم طلا ۱۸: {golds.get('geram18', 'ناموجود')}\n"
            f"مثقال: {golds.get('mesghal', 'ناموجود')}\n"
            f"انس جهانی: $ {golds.get('ounce', 'ناموجود')}\n\n"
            
            f"💰 کریپتو:\n"
            f"تتر: {crypto.get('tether', 'ناموجود')}\n"
            f"بیت‌کوین: $ {crypto.get('bitcoin', 'ناموجود')}\n\n"
            
            f"⏱ آپدیت هر ۱۰ دقیقه"
        )
        return msg
    except Exception as e:
        print("API Error:", e)
        return f"⚠️ خطا در API: {e}"

def auto_send():
    while True:
        bot.send_message(CHAT_ID, get_prices())
        time.sleep(600)  # هر ۱۰ دقیقه

threading.Thread(target=auto_send, daemon=True).start()

@app.route("/")
def home():
    return "Bot Running Successfully"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
