import telebot
import requests
import time
import threading
from flask import Flask
import os

# توکن مستقیم
TOKEN = "1073308116:AAH0mweKwZDPjep9bXq9AQ0Sa6psaP4Q9_k"
CHAT_ID = 714402925

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

API_URL = "https://varzesh3-api.vercel.app/api/prices"

def get_prices():
    try:
        r = requests.get(API_URL, timeout=10)
        if r.status_code != 200 or not r.text.strip():
            return f"⚠️ API پاسخ نداد (کد: {r.status_code})"

        data = r.json()
        print("API Response:", data)  # لاگ برای Railway

        msg = (
            f"🇺🇸 دلار آزاد: {data.get('dollar_free', 'ناموجود')}\n"
            f"🇺🇸 صرافی ملی: {data.get('dollar_national', 'ناموجود')}\n"
            f"🇪🇺 یورو: {data.get('euro', 'ناموجود')}\n"
            f"🇬🇧 پوند: {data.get('pound', 'ناموجود')}\n"
            f"🇹🇷 لیر ترکیه: {data.get('lira', 'ناموجود')}\n\n"
            f"🟡 سکه امامی: {data.get('seke', 'ناموجود')}\n"
            f"🟡 نیم سکه: {data.get('nim', 'ناموجود')}\n"
            f"🟡 ربع سکه: {data.get('rob', 'ناموجود')}\n"
            f"🟡 گرم طلا: {data.get('geram18', 'ناموجود')}\n"
            f"🟡 مثقال: {data.get('mesghal', 'ناموجود')}\n"
            f"🟡 انس طلا: $ {data.get('ounce', 'ناموجود')}\n\n"
            f"💰 تتر: {data.get('tether', 'ناموجود')}\n"
            f"💰 بیت‌کوین: $ {data.get('bitcoin', 'ناموجود')}\n\n"
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
    app.run(host="0.0.0.0", port=port)# -----------------------------
@app.route("/")
def home():
    return "Bot Running OK."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
