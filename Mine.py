# -*- coding: utf-8 -*-
"""
بوت نسخ التداول - معاوية
هذا الكود ينسخ كل العمليات من الحساب الرئيسي إلى الحسابات الفرعية (حتى 15 حساب).
جميع المفاتيح والبيانات تُقرأ من ملف secrets.json
"""

import os
import sys
import json
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

# --------------------------------
# تحميل بيانات API من ملف secrets.json
# --------------------------------
SECRETS_FILE = "secrets.json"

if not os.path.exists(SECRETS_FILE):
    raise FileNotFoundError("⚠️ ملف secrets.json غير موجود. أنشئه وضع فيه المفاتيح.")

with open(SECRETS_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

MAIN_API_KEY    = data.get("main", {}).get("api_key", "")
MAIN_API_SECRET = data.get("main", {}).get("api_secret", "")
SUB_ACCOUNTS    = data.get("subs", [])

# --------------------------------
# إنشاء العملاء (Clients)
# --------------------------------
main_client = Client(MAIN_API_KEY, MAIN_API_SECRET)
sub_clients = [Client(acc["api_key"], acc["api_secret"]) for acc in SUB_ACCOUNTS if acc["api_key"]]

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
