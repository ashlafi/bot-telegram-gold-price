import os
import requests

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
PRICE_API_URL = os.environ.get("PRICE_API_URL")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 OPR/106.0.0.0",
    "Accept": "application/json, text/plain, */*"
}

def get_prices():
    resp = requests.get(PRICE_API_URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()  # خطاهای HTTP را پرتاب می‌کند
    data = resp.json()
    if data.get("status") == 1:
        gold_price = data["data"]["gold"]        # کلیدها را طبق خروجی API تنظیم کن
        currency_price = data["data"]["currency"]
        return gold_price, currency_price
    else:
        raise ValueError("Error fetching prices from API")

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

if __name__ == "__main__":
    gold, usd = get_prices()
    msg = f"💰 قیمت‌ها:\n- طلا: {gold}\n- دلار: {usd}"
    send_message(msg)

