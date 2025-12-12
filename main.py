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
        currencies = requests.get(API_CURRENCIES, timeout=10).json()
        golds = requests.get(API_GOLDS, timeout=10).json()
        crypto = requests.get(API_CRYPTO, timeout=10).json()

        # تاریخ شمسی یا میلادی از یکی از فیلدها
        updated = currencies.get("usd", {}).get("updated_at", "")

        msg = (
            f"💵 ارزها:\n"
            f"🇺🇸 دلار آمریکا: {currencies.get('usd', {}).get('sell', 'ناموجود'):,}\n"
            f"🇺🇸 تتر: {crypto.get('tether', {}).get('sell', 'ناموجود'):,}\n"
            f"🇪🇺 یورو: {currencies.get('eur', {}).get('sell', 'ناموجود'):,}\n"
            f"🇬🇧 پوند انگلیس: {currencies.get('gbp', {}).get('sell', 'ناموجود'):,}\n"
            f"🇨🇦 دلار کانادا: {currencies.get('cad', {}).get('sell', 'ناموجود'):,}\n"
            f"🇦🇪 درهم امارات: {currencies.get('aed', {}).get('sell', 'ناموجود'):,}\n"
            f"🇹🇷 لیر ترکیه: {currencies.get('try', {}).get('sell', 'ناموجود'):,}\n"
            f"🇷🇺 روبل روسیه: {currencies.get('rub', {}).get('sell', 'ناموجود'):,}\n"
            f"🇺🇸 دلار صرافی ملی: {currencies.get('usd_national', {}).get('sell', 'ناموجود'):,}\n\n"

            f"🟡 طلا و سکه:\n"
            f"سکه امامی: {golds.get('seke', {}).get('price', 'ناموجود'):,}\n"
            f"تمام سکه: {golds.get('tamam', {}).get('price', 'ناموجود'):,}\n"
            f"نیم سکه: {golds.get('nim', {}).get('price', 'ناموجود'):,}\n"
            f"ربع سکه: {golds.get('rob', {}).get('price', 'ناموجود'):,}\n"
            f"گرم طلا: {golds.get('geram18', {}).get('price', 'ناموجود'):,}\n"
            f"مثقال طلا: {golds.get('mesghal', {}).get('price', 'ناموجود'):,}\n"
            f"انس طلا: $ {golds.get('ounce', {}).get('price', 'ناموجود'):,}\n\n"

            f"💰 کریپتو:\n"
            f"بیت کوین: $ {crypto.get('bitcoin', {}).get('sell', 'ناموجود'):,}\n\n"

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
        time.sleep(600)  # هر ۱۰ دقیقه

threading.Thread(target=auto_send, daemon=True).start()

@app.route("/")
def home():
    return "Bot Running Successfully"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
