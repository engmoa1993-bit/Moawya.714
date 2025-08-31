# -*- coding: utf-8 -*-
"""
بوت نسخ التداول - معاوية
هذا الكود ينسخ كل العمليات من الحساب الرئيسي إلى الحسابات الفرعية (حتى 15 حساب).
"""

import os
import sys
import subprocess

# -------------------------------
# تثبيت المكتبات إذا غير موجودة
# -------------------------------
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from binance.client import Client
    from binance.enums import *
except ImportError:
    install("python-binance")
    from binance.client import Client
    from binance.enums import *

try:
    import pandas as pd
except ImportError:
    install("pandas")
    import pandas as pd

# --------------------------------
# 🔑 ضع هنا بيانات الحساب الرئيسي
# --------------------------------
MAIN_API_KEY    = "💚_ضع_مفتاح_API_الحساب_الرئيسي_هنا"
MAIN_API_SECRET = "💚_ضع_الرقم_السري_للحساب_الرئيسي_هنا"

# --------------------------------
# 🔑 ضع هنا بيانات الحسابات الفرعية
# --------------------------------
SUB_ACCOUNTS = [
    {"api_key": "💚_ضع_API_الفرعي1", "api_secret": "💚_ضع_SECRET_الفرعي1"},
    {"api_key": "💚_ضع_API_الفرعي2", "api_secret": "💚_ضع_SECRET_الفرعي2"},
    {"api_key": "💚_ضع_API_الفرعي3", "api_secret": "💚_ضع_SECRET_الفرعي3"},
    {"api_key": "💚_ضع_API_الفرعي4", "api_secret": "💚_ضع_SECRET_الفرعي4"},
    {"api_key": "💚_ضع_API_الفرعي5", "api_secret": "💚_ضع_SECRET_الفرعي5"},
    {"api_key": "💚_ضع_API_الفرعي6", "api_secret": "💚_ضع_SECRET_الفرعي6"},
    {"api_key": "💚_ضع_API_الفرعي7", "api_secret": "💚_ضع_SECRET_الفرعي7"},
    {"api_key": "💚_ضع_API_الفرعي8", "api_secret": "💚_ضع_SECRET_الفرعي8"},
    {"api_key": "💚_ضع_API_الفرعي9", "api_secret": "💚_ضع_SECRET_الفرعي9"},
    {"api_key": "💚_ضع_API_الفرعي10", "api_secret": "💚_ضع_SECRET_الفرعي10"},
    {"api_key": "💚_ضع_API_الفرعي11", "api_secret": "💚_ضع_SECRET_الفرعي11"},
    {"api_key": "💚_ضع_API_الفرعي12", "api_secret": "💚_ضع_SECRET_الفرعي12"},
    {"api_key": "💚_ضع_API_الفرعي13", "api_secret": "💚_ضع_SECRET_الفرعي13"},
    {"api_key": "💚_ضع_API_الفرعي14", "api_secret": "💚_ضع_SECRET_الفرعي14"},
    {"api_key": "💚_ضع_API_الفرعي15", "api_secret": "💚_ضع_SECRET_الفرعي15"},
]

# --------------------------------
# إنشاء العملاء (Clients)
# --------------------------------
main_client = Client(MAIN_API_KEY, MAIN_API_SECRET)
sub_clients = [Client(acc["api_key"], acc["api_secret"]) for acc in SUB_ACCOUNTS if acc["api_key"] != ""]

print("✅ تم الاتصال بالحساب الرئيسي والفرعي بنجاح.")

# --------------------------------
# دالة نسخ الأوامر
# --------------------------------
def copy_order(order):
    symbol   = order["symbol"]
    side     = order["side"]
    o_type   = order["type"]
    quantity = order["origQty"]

    print(f"📌 نسخ أمر: {side} {quantity} {symbol}")

    for i, client in enumerate(sub_clients, start=1):
        try:
            client.create_order(
                symbol=symbol,
                side=side,
                type=o_type,
                quantity=quantity
            )
            print(f"   ✅ نُفِّذ في الحساب الفرعي {i}")
        except Exception as e:
            print(f"   ❌ خطأ في الحساب الفرعي {i}: {e}")

# --------------------------------
# متابعة أوامر الحساب الرئيسي
# --------------------------------
def main_loop():
    print("🚀 بدأ البوت متابعة أوامر الحساب الرئيسي...")
    from time import sleep

    while True:
        try:
            orders = main_client.get_all_orders(symbol="BTCUSDT", limit=1)
            if orders:
                last_order = orders[-1]
                copy_order(last_order)
        except Exception as e:
            print(f"⚠️ خطأ: {e}")
        sleep(10)  # فحص كل 10 ثواني

if __name__ == "__main__":
    main_loop()
