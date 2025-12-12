# save as price_bot.py
import requests
import time

TELEGRAM_BOT_TOKEN = "1073308116:AAH0mweKwZDPjep9bXq9AQ0Sa6psaP4Q9_k"
CHAT_ID = "714402925"  # یا آی‌دی کانال (با @channelusername هم میشه ولی باید ربات ادمین باشه)

# --- Endpoints / config ---
EXCH_HOST = "https://api.exchangerate.host/latest"
COINGECKO_SIMPLE = "https://api.coingecko.com/api/v3/simple/price"
# TGJU unofficial JSON endpoint (community wrappers) - استفاده به عنوان منبع سکه/طلا ایران
TGJU_GOLD_API = "https://tgju.amirhossein.info/api/price/gold"   # ممکنه در دسترس نباشد
PRICEDAY_USD_IRR = "https://api.priceto.day/v1/latest/irr/usd"   # نمونه از PriceDB/priceto.day

def fetch_usd_to_irr():
    # اول تلاش به priceto.day (مخصوص ایران)
    try:
        r = requests.get(PRICEDAY_USD_IRR, timeout=6)
        j = r.json()
        # فرض می‌کنیم خروجی {'price': 125700000} یا مشابه؛ اگر ساختار فرق داشت، نیاز به تنظیم دارد
        # این API ها گوناگون هستند؛ در عمل باید پاسخ را مطابق نمونه‌ی واقعی‌شان parse کنید.
        if isinstance(j, dict):
            # بعضی endpointها structure مختلف دارند — تلاش برای چند کلید رایج:
            for key in ("price","value","data","rate"):
                if key in j:
                    return float(j[key])
            # گاهی پاسخ دقیقا {'usd': 125700}
            if "usd" in j:
                return float(j["usd"])
    except Exception:
        pass

    # fallback: exchangerate.host (نسبتاً پایدار) — تبدیل USD -> IRR (اگر موجود باشد)
    try:
        r = requests.get(EXCH_HOST + "?base=USD&symbols=IRR", timeout=6)
        jr = r.json()
        rate = jr.get("rates", {}).get("IRR")
        if rate:
            return float(rate)
    except Exception:
        pass

    raise RuntimeError("Couldn't fetch USD→IRR rate from any source")

def fetch_forex_rates():
    # می‌گیریم: EUR,GBP,CAD,AED,TRY,RUB relative به USD و سپس به IRR تبدیل می‌کنیم
    symbols = "EUR,GBP,CAD,AED,TRY,RUB"
    r = requests.get(EXCH_HOST + f"?base=USD&symbols={symbols}", timeout=6)
    data = r.json()
    rates = data.get("rates", {})
    return rates  # مثلاً {'EUR': 0.92, ...} meaning 1 USD = 0.92 EUR

def fetch_crypto_prices():
    # CoinGecko simple price
    params = {"ids":"bitcoin,tether","vs_currencies":"usd"}
    r = requests.get(COINGECKO_SIMPLE, params=params, timeout=6)
    return r.json()  # {'bitcoin': {'usd': 90049}, 'tether': {'usd': 1.0}}

def fetch_tgju_gold():
    # این endpoint ممکن است در دسترس باشد یا JSON متفاوت بازگرداند — در صورت نیاز parse را اصلاح کن
    try:
        r = requests.get(TGJU_GOLD_API, timeout=6)
        return r.json()
    except Exception:
        return None

def format_message():
    usd_to_irr = fetch_usd_to_irr()
    forex = fetch_forex_rates()  # مقادیر نسبت به USD
    crypto = fetch_crypto_prices()
    tgju = fetch_tgju_gold()

    # محاسبه نرخ‌ها به ریال (نمونه): USD (ارزش بازار آزاد) = usd_to_irr
    usd = usd_to_irr
    # تتر ~ قیمت دلاری * تبدیل (معمولاً 1-1 با USD ولی در ایران گاهی تفاوت دارد)
    tether_usd = crypto.get("tether", {}).get("usd", 1.0)
    tether_irr = tether_usd * usd_to_irr
    btc_usd = crypto.get("bitcoin", {}).get("usd", 0)
    btc_display = f"${int(btc_usd):,}"

    # سایر ارزها: نیاز داریم نرخ هر ارز نسبت به USD را گرفته و در usd_to_irr ضرب کنیم:
    def to_irr_from_usdrate(rate_against_usd):
        # اگر rate = (1 USD = X EUR) ، برای تبدیل 1 EUR -> IRR: (1 EUR) = (1 / rate) USD -> * usd_to_irr
        if not rate_against_usd or rate_against_usd == 0: return None
        eur_to_irr = (1.0 / rate_against_usd) * usd_to_irr
        return eur_to_irr

    eur_irr = to_irr_from_usdrate(forex.get("EUR"))
    gbp_irr = to_irr_from_usdrate(forex.get("GBP"))
    cad_irr = to_irr_from_usdrate(forex.get("CAD"))
    aed_irr = to_irr_from_usdrate(forex.get("AED"))
    try_irr = to_irr_from_usdrate(forex.get("TRY"))
    rub_irr = to_irr_from_usdrate(forex.get("RUB"))

    # نمونه سکه/طلا از TGJU (اگر در دسترس باشد parse کن، در غیر اینصورت placeholder)
    if tgju and isinstance(tgju, dict):
        # فرض می‌کنیم داده‌ها کلیدهای مشخصی دارند؛ در پروژه واقعی باید از ساختار JSON واقعی استفاده کنی
        sekeh_emami = tgju.get("sekeh_emami") or tgju.get("Imami") or "N/A"
        gram_tala = tgju.get("gram18") or tgju.get("gram") or "N/A"
    else:
        sekeh_emami = "N/A"
        gram_tala = "N/A"

    # ساخت پیام مطابق نمونه‌ی تو
    lines = []
    lines.append(f"🇺🇸 دلار آمریکا: {int(usd):,}")
    lines.append(f"🇺🇸 تتر: {int(tether_irr):,}")
    lines.append(f"🇪🇺 یورو: {int(eur_irr) if eur_irr else 'N/A'}")
    lines.append(f"🇬🇧 پوند انگلیس: {int(gbp_irr) if gbp_irr else 'N/A'}")
    lines.append(f"🇨🇦 دلار کانادا: {int(cad_irr) if cad_irr else 'N/A'}")
    lines.append(f"🇦🇪 درهم امارات: {int(aed_irr) if aed_irr else 'N/A'}")
    lines.append(f"🇹🇷 لیر ترکیه: {int(try_irr) if try_irr else 'N/A'}")
    lines.append(f"🇷🇺 روبل روسیه: {int(rub_irr) if rub_irr else 'N/A'}")
    lines.append(f"🇺🇸 دلار صرافی ملی: {int(usd):,}")  # می‌تونی مقدار متفاوتی بذاری اگر منبع جدا داری
    lines.append(f"🟡 سکه امامی: {sekeh_emami}")
    lines.append(f"🟡 گرم طلا: {gram_tala}")
    lines.append(f"💰 بیت کوین: {btc_display}")
    lines.append("")
    lines.append("📮 " + time.strftime("%Y-%m-%d"))

    return "\n".join(lines)

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    r = requests.post(url, data=payload, timeout=10)
    return r.json()

if __name__ == "__main__":
    try:
        msg = format_message()
        res = send_telegram_message(msg)
        print("sent:", res)
    except Exception as e:
        print("error:", e)
