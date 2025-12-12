import telebot
import requests
import time
import threading
from flask import Flask

TOKEN = "1073308116:AAH0mweKwZDPjep9bXq9AQ0Sa6psaP4Q9_k"
CHAT_ID = 714402925

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# -----------------------------
# گرفتن اطلاعات
# -----------------------------
def get_all_prices():
    try:
        # ارزها
        fx = requests.get("https://api.tgju.online/v1/data/sana/all").json()["data"]
        # طلا و سکه
        gold = requests.get("https://api.tgju.online/v1/data/gold/all").json()["data"]
        # ارزهای دیجیتال
        crypto = requests.get("https://api.tgju.online/v1/data/crypto/all").json()["data"]

        msg = (
            f"🇺🇸 دلار آمریکا: {fx['usd']['p']}\n"
            f"🇺🇸 تتر: {crypto['tether']['p']}\n"
            f"🇪🇺 یورو: {fx['eur']['p']}\n"
            f"🇬🇧 پوند انگلیس: {fx['gbp']['p']}\n"
            f"🇨🇦 دلار کانادا: {fx['cad']['p']}\n"
            f"🇦🇪 درهم امارات: {fx['aed']['p']}\n"
            f"🇹🇷 لیر ترکیه: {fx['try']['p']}\n"
            f"🇷🇺 روبل روسیه: {fx['rub']['p']}\n"
            f"🇺🇸 دلار صرافی ملی: {fx['usd_sana']['p']}\n\n"
            f"🟡 سکه امامی: {gold['sekke_emami']['p']}\n"
            f"🟡 تمام سکه: {gold['sekke_bahar']['p']}\n"
            f"🟡 نیم سکه: {gold['nim']['p']}\n"
            f"🟡 ربع سکه: {gold['rob']['p']}\n"
            f"🟡 گرم طلا: {gold['geram18']['p']}\n"
            f"🟡 مثقال طلا: {gold['mesghal']['p']}\n"
            f"🟡 انس طلا: $ {gold['ons']['p']}\n\n"
            f"💰 بیت‌کوین: $ {crypto['bitcoin']['p']}\n\n"
            f"📮 آپدیت خودکار هر ۱۰ دقیقه\n"
            f"#طلا #دلار #ارز #سکه #بیتکوین"
        )

        return msg

    except Exception as e:
        return f"خطا در دریافت اطلاعات: {e}"


# -----------------------------
# ارسال خودکار
# -----------------------------
def auto_send():
    while True:
        price_msg = get_all_prices()

        try:
            bot.send_message(CHAT_ID, price_msg)
        except:
            pass

        time.sleep(600)  # هر 10 دقیقه


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
