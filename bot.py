import os
import requests
import datetime
import jdatetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PRICE_API_URL = os.getenv("PRICE_API_URL")

headers = {
    "User-Agent": "Mozilla/5.0"
}

def format_number(num):
    """سه رقم سه رقم جدا کردن اعداد با ویرگول فارسی"""
    try:
        return "{:,}".format(int(num)).replace(",", "٬")
    except:
        return str(num)

def is_holiday():
    """بررسی تعطیل بودن روز جاری از holidayapi.ir"""
    today = jdatetime.date.today()
    url = f"https://holidayapi.ir/jalali/{today.year}/{today.month}/{today.day}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("is_holiday", False), data.get("events", [])
        else:
            print(f"❌ Error holiday api: {resp.status_code}")
            return False, []
    except Exception as e:
        print(f"❌ Exception holiday api: {e}")
        return False, []

def get_prices():
    """دریافت قیمت‌ها از API"""
    resp = requests.get(PRICE_API_URL, headers=headers, timeout=10)
    data = resp.json()

    gold_list = data['gold']
    currency_list = data['currency']

    gold_18 = next((item for item in gold_list if item['symbol'] == 'IR_GOLD_18K'), None)
    gold_24 = next((item for item in gold_list if item['symbol'] == 'IR_GOLD_24K'), None)
    coin_1g = next((item for item in gold_list if item['symbol'] == 'IR_COIN_1G'), None)
    coin_quarter = next((item for item in gold_list if item['symbol'] == 'IR_COIN_QUARTER'), None)
    coin_half = next((item for item in gold_list if item['symbol'] == 'IR_COIN_HALF'), None)
    coin_emami = next((item for item in gold_list if item['symbol'] == 'IR_COIN_EMAMI'), None)

    usd = next((item for item in currency_list if item['symbol'] == 'USD'), None)
    eur = next((item for item in currency_list if item['symbol'] == 'EUR'), None)

    return gold_18, gold_24, coin_1g, coin_quarter, coin_half, coin_emami, usd, eur

def build_message(include_header=False, events=None):
    """ساخت متن پیام تلگرام"""
    gold_18, gold_24, coin_1g, coin_quarter, coin_half, coin_emami, usd, eur = get_prices()

    header = ""
    if include_header:
        header = "📅 امروز تعطیل رسمی است"
        if events:
            # فقط توضیحات تعطیل‌ها رو اضافه کن
            holidays = [e["description"] for e in events if e.get("is_holiday")]
            if holidays:
                header += f" ({'، '.join(holidays)})"
        header += "\n\n"

    msg = (
        f"{header}"
        f"💰 طلا 18 عیار: {format_number(gold_18['price'])} {gold_18['unit']}\n"
        f"💰 طلا 24 عیار: {format_number(gold_24['price'])} {gold_24['unit']}\n\n"
        f"🪙 سکه یک گرمی: {format_number(coin_1g['price'])} {coin_1g['unit']}\n"
        f"🪙 ربع سکه: {format_number(coin_quarter['price'])} {coin_quarter['unit']}\n"
        f"🪙 نیم سکه: {format_number(coin_half['price'])} {coin_half['unit']}\n"
        f"🪙 سکه امامی: {format_number(coin_emami['price'])} {coin_emami['unit']}\n\n"
        f"💵 دلار آمریکا: {format_number(usd['price'])} {usd['unit']}\n"
        f"💶 یورو: {format_number(eur['price'])} {eur['unit']}\n\n"
        f"@dollar_gold_price_now"
    )
    return msg

def send_message(text):
    """ارسال پیام به تلگرام"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

if __name__ == "__main__":
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute

    try:
        holiday, events = is_holiday()

        if holiday:
            # روز تعطیل → فقط یکبار 12 ظهر
            if hour == 12 and minute < 5:
                msg = build_message(include_header=True, events=events)
                send_message(msg)
        else:
            # روز عادی → فقط بین 10 صبح تا 8 شب
            if 10 <= hour < 20:
                msg = build_message()
                send_message(msg)

    except Exception as e:
        print(f"❌ Exception main: {e}")
