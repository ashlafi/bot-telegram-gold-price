import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PRICE_API_URL = os.getenv("PRICE_API_URL")

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_prices():
    resp = requests.get(PRICE_API_URL, headers=headers, timeout=10)
    data = resp.json()

    gold_list = data['gold']
    currency_list = data['currency']

    # پیدا کردن قیمت طلا 18 عیار
    gold_price = next((item['price'] for item in gold_list if item.get('name_en') == '18K Gold' or item.get('name') == 'طلای 18 عیار'), None)
    # پیدا کردن قیمت دلار
    usd_price = next((item['price'] for item in currency_list if item.get('name_en') == 'USD' or item.get('symbol') == 'USD'), None)

    return gold_price, usd_price

def format_number(num):
    """تبدیل عدد به فرمت سه رقم سه رقم با کاما"""
    try:
        return "{:,}".format(int(num))
    except:
        return str(num)

gold_price, usd_price = get_prices()

msg = (
    f"قیمت طلا 18 عیار 💰: {format_number(gold_price)} تومان\n\n"
    f"قیمت دلار بازار آزاد 💵: {format_number(usd_price)} تومان\n\n"
    f"@dollar_gold_price_now"
)

requests.get(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    params={"chat_id": CHAT_ID, "text": msg}
)
