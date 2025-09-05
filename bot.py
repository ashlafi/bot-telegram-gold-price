import os
import requests
import jdatetime
from datetime import datetime
import pytz

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PRICE_API_URL = os.getenv("PRICE_API_URL")

headers = {
    "User-Agent": "Mozilla/5.0"
}

def format_number(num):
    """سه رقم سه رقم جدا کردن اعداد با کامای انگلیسی"""
    try:
        return "{:,}".format(int(num))
    except:
        return str(num)

def is_holiday():
    """بررسی تعطیل بودن روز جاری از طریق holidayapi.ir"""
    today = jdatetime.date.today()
    url = f"https://holidayapi.ir/jalali/{today.year}/{today.month}/{today.day}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        return data.get("is_holiday", False)
    except Exception as e:
        print("خطا در بررسی تعطیلی:", e)
        return False

def is_allowed_time():
    """بررسی بازه مجاز ارسال پیام بر اساس ساعت ایران"""
    tz = pytz.timezone("Asia/Tehran")
    now = datetime.now(tz)
    hour = now.hour

    if is_holiday():
        # روز تعطیل → فقط ۱۲ تا ۱۳ و ۱۷ تا ۱۸
        return (12 <= hour < 13) or (17 <= hour < 18)
    else:
        # روز عادی → ۱۰ صبح تا ۸ شب
        return 10 <= hour < 20

def get_prices():
    resp = requests.get(PRICE_API_URL, headers=headers, timeout=10)
    data = resp.json()

    gold_list = data['gold']
    currency_list = data['currency']

    gold_18 = next((item for item in gold_list if item['symbol'] == 'IR_GOLD_18K'), None)
    gold_24 = next((item for item in gold_list if item['symbol'] == 'IR_GOLD_24K'), None)
    coin_1g = next((item for item in gold_list if item['symbol'] == 'IR_COIN_1G'), None)
    coin_quarter = next((item for item in gold_list if item['symbol'] == 'IR_COIN_
