# -*- coding: utf-8 -*-
"""
بوت نسخ التداول - معرب وجاهز للعمل
يدعم Spot وFutures
ينسخ كل الصفقات من الحساب الرئيسي إلى الحسابات الفرعية
"""

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# تثبيت المكتبات
try:
    import pandas as pd
except:
    install("pandas")
    import pandas as pd

try:
    from binance.client import Client
    from binance.enums import *
except:
    install("python-binance")
    from binance.client import Client
    from binance.enums import *

import time

# ------------- الحساب الرئيسي -------------
main_account = {
    "name": "الحساب الرئيسي",
    "api_key": "ضع_API_KEY_الرئيسي_هنا",      # 💚 انسخ والصق هنا
    "api_secret": "ضع_API_SECRET_الرئيسي_هنا" # 💚 انسخ والصق هنا
}

# ------------- الحسابات الفرعية -------------
sub_accounts = [
    {"name": "فرعي 1", "api_key": "API_KEY1_هنا💚", "api_secret": "API_SECRET1_هنا💚"},
    {"name": "فرعي 2", "api_key": "API_KEY2_هنا💚", "api_secret": "API_SECRET2_هنا💚"},
    {"name": "فرعي 3", "api_key": "API_KEY3_هنا💚", "api_secret": "API_SECRET3_هنا💚"},
    {"name": "فرعي 4", "api_key": "API_KEY4_هنا💚", "api_secret": "API_SECRET4_هنا💚"},
    {"name": "فرعي 5", "api_key": "API_KEY5_هنا💚", "api_secret": "API_SECRET5_هنا💚"},
    {"name": "فرعي 6", "api_key": "API_KEY6_هنا💚", "api_secret": "API_SECRET6_هنا💚"},
    {"name": "فرعي 7", "api_key": "API_KEY7_هنا💚", "api_secret": "API_SECRET7_هنا💚"},
    {"name": "فرعي 8", "api_key": "API_KEY8_هنا💚", "api_secret": "API_SECRET8_هنا💚"},
    {"name": "فرعي 9", "api_key": "API_KEY9_هنا💚", "api_secret": "API_SECRET9_هنا💚"},
    {"name": "فرعي 10", "api_key": "API_KEY10_هنا💚", "api_secret": "API_SECRET10_هنا💚"},
    {"name": "فرعي 11", "api_key": "API_KEY11_هنا💚", "api_secret": "API_SECRET11_هنا💚"},
    {"name": "فرعي 12", "api_key": "API_KEY12_هنا💚", "api_secret": "API_SECRET12_هنا💚"},
    {"name": "فرعي 13", "api_key": "API_KEY13_هنا💚", "api_secret": "API_SECRET13_هنا💚"},
    {"name": "فرعي 14", "api_key": "API_KEY14_هنا💚", "api_secret": "API_SECRET14_هنا💚"},
    {"name": "فرعي 15", "api_key": "API_KEY15_هنا💚", "api_secret": "API_SECRET15_هنا💚"},
]

# ------------- إنشاء عملاء Binance لكل حساب -------------
main_client = Client(main_account["api_key"], main_account["api_secret"])
sub_clients = []
for acc in sub_accounts:
    sub_clients.append(Client(acc["api_key"], acc["api_secret"]))

# ------------- دالة نسخ الصفقات -------------
def copy_trade_to_sub_accounts(symbol, side, order_type, quantity, price=None, futures=False):
    for i, client in enumerate(sub_clients):
        try:
            if futures:
                if order_type == "MARKET":
                    client.futures_create_order(symbol=symbol, side=side, type=ORDER_TYPE_MARKET, quantity=quantity)
                elif order_type == "LIMIT":
                    client.futures_create_order(symbol=symbol, side=side, type=ORDER_TYPE_LIMIT, timeInForce=TIME_IN_FORCE_GTC, quantity=quantity, price=str(price))
            else:
                if order_type == "MARKET":
                    client.create_order(symbol=symbol, side=side, type=ORDER_TYPE_MARKET, quantity=quantity)
                elif order_type == "LIMIT":
                    client.create_order(symbol=symbol, side=side, type=ORDER_TYPE_LIMIT, timeInForce=TIME_IN_FORCE_GTC, quantity=quantity, price=str(price))
            print(f"✅ تم تنفيذ الصفقة في الحساب الفرعي: {sub_accounts[i]['name']}")
        except Exception as e:
            print(f"❌ خطأ في الحساب الفرعي {sub_accounts[i]['name']}: {e}")

# ------------- تنفيذ الصفقة في الحساب الرئيسي -------------
def execute_main_trade(symbol, side, order_type, quantity, price=None, futures=False):
    try:
        if futures:
            if order_type == "MARKET":
                main_client.futures_create_order(symbol=symbol, side=side, type=ORDER_TYPE_MARKET, quantity=quantity)
            elif order_type == "LIMIT":
                main_client.futures_create_order(symbol=symbol, side=side, type=ORDER_TYPE_LIMIT, timeInForce=TIME_IN_FORCE_GTC, quantity=quantity, price=str(price))
        else:
            if order_type == "MARKET":
                main_client.create_order(symbol=symbol, side=side, type=ORDER_TYPE_MARKET, quantity=quantity)
            elif order_type == "LIMIT":
                main_client.create_order(symbol=symbol, side=side, type=ORDER_TYPE_LIMIT, timeInForce=TIME_IN_FORCE_GTC, quantity=quantity, price=str(price))
        print("✅ تم تنفيذ الصفقة في الحساب الرئيسي")
        copy_trade_to_sub_accounts(symbol, side, order_type, quantity, price, futures)
    except Exception as e:
        print("❌ خطأ في الحساب الرئيسي:", e)

# ---------------- مثال للتجربة ----------------
symbol = "BTCUSDT"
side = "BUY"
order_type = "MARKET"
quantity = 0.001
price = None
futures = False  # False للـSpot، True للفيوتشرز

execute_main_trade(symbol, side, order_type, quantity, price, futures)
