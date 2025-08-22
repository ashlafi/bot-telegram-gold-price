import os
import requests

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
PRICE_API_URL = os.environ.get("PRICE_API_URL")

def get_prices():
    resp = requests.get(PRICE_API_URL)
    data = resp.json()
    gold = data['gold']  # بر اساس خروجی API تغییر بده
    usd = data['usd']
    return gold, usd

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

g,u = get_prices()
send_message(f"💰 قیمت:\nطلا: {g}\nدلار: {u}")
