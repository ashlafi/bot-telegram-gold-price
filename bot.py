import os
import requests
from datetime import datetime
import pytz

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PRICE_API_URL = os.getenv("PRICE_API_URL")
HOLIDAY_API = "https://holidayapi.ir/jalali"

headers = {"User-Agent": "Mozilla/5.0"}

def format_number(num):
    """فرمت اعداد با جداکننده انگلیسی"""
    try:
        return "{:,}".format(int(num))
    except:
        return str(num)

def get_prices():
    resp = requests.get(PRICE_API_URL, headers=headers, timeout=15)
    return resp.json()

def get_holiday_status(year, month, day):
    url = f"{HOLIDAY_API}/{year}/{month}/{day}"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        return resp.json().get("is_holiday", False)
    except:
        return False

def build_normal_message(data):
    gold_list = data["gold"]
    currency_list = data["currency"]

    def find(symbol, source):
        return next((item for item in source if item["symbol"] == symbol), None)

    gold_18 = find("IR_GOLD_18K", gold_list)
    gold_24 = find("IR_GOLD_24K", gold_list)
    coin_1g = find("IR_COIN_1G", gold_list)
    coin_quarter = find("IR_COIN_QUARTER", gold_list)
    coin_half = find("IR_COIN_HALF", gold_list)
    coin_emami = find("IR_COIN_EMAMI", gold_list)

    usd = find("USD", currency_list)
    eur = find("EUR", currency_list)

    msg = (
        f"💰 طلا 18 عیار: {format_number(gold_18['price'])} {gold_18['unit']}\n"
        f"💰 طلا 24 عیار: {format_number(gold_24['price'])} {gold_24['unit']}\n\n"
        f"🪙 سکه یک گرمی: {format_number(coin_1g['price'])} {coin_1g['unit']}\n"
        f"🪙 ربع سکه: {format_number(coin_quarter['price'])} {coin_quarter['unit']}\n"
        f"🪙 نیم سکه: {format_number(coin_half['price'])} {coin_half['unit']}\n"
        f"🪙 سکه امامی: {format_number(coin_emami['price'])} {coin_emami['unit']}\n\n"
        f"💵 دلار: {format_number(usd['price'])} {usd['unit']}\n"
        f"💶 یورو: {format_number(eur['price'])} {eur['unit']}\n\n"
        f"@dollar_gold_price_now"
    )
    return msg

def build_full_message(data):
    gold_list = data["gold"]
    currency_list = data["currency"]

    gold_msg = "🏅 قیمت طلا و سکه:\n"
    for item in gold_list:
        gold_msg += f"{item['name']}: {format_number(item['price'])} {item['unit']}\n"

    currency_msg = "\n💱 قیمت ارزها:\n"
    for item in currency_list:
        currency_msg += f"{item['name']}: {format_number(item['price'])} {item['unit']}\n"

    return gold_msg + currency_msg + "\n\n@dollar_gold_price_now"

def send_message(text):
    try:
        requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": text},
            timeout=15
        )
    except Exception as e:
        print("❌ Error sending message:", e)

if __name__ == "__main__":
    tz = pytz.timezone("Asia/Tehran")
    now = datetime.now(tz)

    year, month, day = now.year, now.month, now.day
    is_holiday = get_holiday_status(year, month, day)

    data = get_prices()

    if not is_holiday:
        # روزهای عادی
        if 10 <= now.hour < 20:
            msg = build_normal_message(data)
            send_message(msg)

        # ارسال گزارش کامل یکبار در بازه 11 تا 11:30
        if now.hour == 11 and now.minute < 30:
            msg_full = build_full_message(data)
            send_message("📊 گزارش کامل بازار امروز:\n\n" + msg_full)

    else:
        # روزهای تعطیل → فقط دو بازه
        if 11 <= now.hour < 12 or 17 <= now.hour < 18:
            msg = build_normal_message(data)
            send_message(msg)
