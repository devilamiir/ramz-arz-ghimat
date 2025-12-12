import requests
from flask import Flask, request

# --------------------------
# تنظیمات
# --------------------------
BOT_TOKEN = "1073308116:AAH0mweKwZDPjep9bXq9AQ0Sa6psaP4Q9_k"
CHAT_ID = "714402925"

# API های رایگان استفاده شده:
API_USD = "https://api.priceto.day/v1/latest/irr/usd"
API_TETHER = "https://api.coingecko.com/api/v3/simple/price?ids=tether,bitcoin&vs_currencies=usd"
API_TGJU = "https://api.tgju.org/v1/latest/list"

app = Flask(name)

# --------------------------
# گرفتن قیمت دلار آزاد
# --------------------------
def get_usd():
    try:
        r = requests.get(API_USD, timeout=5).json()
        return int(r.get("data", {}).get("price", 0))
    except:
        return 0

# --------------------------
# گرفتن قیمت تتر و بیت‌کوین (دلاری)
# --------------------------
def get_crypto():
    try:
        r = requests.get(API_TETHER, timeout=5).json()
        tether_usd = r["tether"]["usd"]
        btc_usd = r["bitcoin"]["usd"]
        return tether_usd, btc_usd
    except:
        return 1, 0

# --------------------------
# گرفتن قیمت سکه و طلا از TGJU
# --------------------------
def get_gold_tgju():
    try:
        r = requests.get(API_TGJU, timeout=5).json()
        data = r.get("data", {})

        emami = int(data["sekeh_emi"]["p"])
        sekke_full = int(data["sekeh"]["p"])
        nim = int(data["nim"]["p"])
        rob = int(data["rob"]["p"])
        gram = int(data["geram18"]["p"])
        mesghal = int(data["mesghal"]["p"])
        ons = float(data["ons"]["p"])

        return emami, sekke_full, nim, rob, gram, mesghal, ons
    except:
        return [0]*7

# --------------------------
# ساخت پیام نهایی
# --------------------------
def build_message():
    usd = get_usd()

    tether_usd, btc_usd = get_crypto()
    tether_irr = int(tether_usd * usd)

    emami, full_s, nim_s, rob_s, gram_t, mesghal_t, ons = get_gold_tgju()

    msg = f"""
🇺🇸 دلار آمریکا: {usd:,}
🇺🇸 تتر: {tether_irr:,}
🇪🇺 یورو: ❌ API رایگان دقیق ندارد
🇬🇧 پوند انگلیس: ❌
🇨🇦 دلار کانادا: ❌
🇦🇪 درهم امارات: ❌
🇹🇷 لیر ترکیه: ❌
🇷🇺 روبل روسیه: ❌
🇺🇸 دلار صرافی ملی: ❌

🟡 سکه امامی: {emami:,}
🟡 تمام سکه: {full_s:,}
🟡 نیم سکه: {nim_s:,}
🟡 ربع سکه: {rob_s:,}
🟡 گرم طلا: {gram_t:,}
🟡 مثقال طلا: {mesghal_t:,}
🟡 انس طلا: $ {ons}

💰 بیت کوین: $ {btc_usd:,}

📮 قیمت لحظه‌ای
#طلا #دلار #بیتکوین #سکه
"""
    return msg

# --------------------------
# ارسال پیام به تلگرام
# --------------------------
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

# --------------------------
# روت اجرای اتوماتیک
# --------------------------
@app.route("/")
def home():
    return "Price Bot is Running."

@app.route("/send")
def send():
    msg = build_message()
    send_message(msg)
    return "Message Sent!"

# --------------------------
# اجرای برنامه
# --------------------------
if name == "main":
    app.run(host="0.0.0.0", port=8080)
