import os
import requests

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

def get_prices():
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

gold_18, gold_24, coin_1g, coin_quarter, coin_half, coin_emami, usd, eur = get_prices()

msg = (
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

requests.get(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    params={"chat_id": CHAT_ID, "text": msg}
)
