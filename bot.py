import os
import requests

PRICE_API_URL = os.environ['PRICE_API_URL']
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/106.0.0.0",
    "Accept": "application/json, text/plain, */*"
}

def get_prices():
    resp = requests.get(PRICE_API_URL, headers=headers, timeout=10)
    data = resp.json()
    gold = data['gold']['geram18']['price']
    usd = data['currency']['usd']['price']
    return gold, usd

gold_price, usd_price = get_prices()

message = f"💰 قیمت طلا: {gold_price}\n💵 قیمت دلار: {usd_price}"
requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", params={"chat_id": CHAT_ID, "text": message})
