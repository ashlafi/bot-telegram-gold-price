import requests
import time
import os

TOKEN = os.environ.get("7484847090:AAHBjVKGCSOfsVwvFcXBFRcwbXZMhVMIYfk")
CHAT_ID = os.environ.get("https://t.me/dollar_gold_price_now")
PRICE_API_URL = os.environ.get("BNWws2fmDNyP2hCajebeBxVjnnsqec7E")

def get_prices():
    r = requests.get(PRICE_API_URL)
    data = r.json()
    gold = data['gold']  # تغییر طبق API
    usd = data['usd']
    return gold, usd

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

while True:
    try:
        g, u = get_prices()
        msg = f"💰 قیمت:\n- طلا: {g}\n- دلار: {u}"
        send_message(msg)
    except Exception as e:
        print("خطا:", e)
    time.sleep(300)
