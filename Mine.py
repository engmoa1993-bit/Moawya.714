# -*- coding: utf-8 -*-
"""
بوت نسخ التداول - معاوية
يقوم بنسخ كل الأوامر من الحساب الرئيسي إلى الحسابات الفرعية (حتى 15 حساب).
النسخ فوري باستخدام WebSocket stream من Binance.
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
    from binance.streams import ThreadedWebsocketManager
except ImportError:
    install("python-binance")
    from binance.client import Client
    from binance.enums import *
    from binance.streams import ThreadedWebsocketManager

# --------------------------------
# تحميل بيانات API من أداة Secrets
# --------------------------------
MAIN_API_KEY    = os.getenv("MAIN_API_KEY")
MAIN_API_SECRET = os.getenv("MAIN_API_SECRET")

if not MAIN_API_KEY or not MAIN_API_SECRET:
    raise ValueError("⚠️ تأكد من إضافة MAIN_API_KEY و MAIN_API_SECRET في أداة Secrets.")

# الحسابات الفرعية (حتى 15 حساب)
SUB_ACCOUNTS = []
for i in range(1, 16):
    key = os.getenv(f"SUB{i}_API_KEY")
    secret = os.getenv(f"SUB{i}_API_SECRET")
    if key and secret:
        SUB_ACCOUNTS.append({"api_key": key, "api_secret": secret})

# --------------------------------
# إنشاء العملاء (Clients)
# --------------------------------
main_client = Client(MAIN_API_KEY, MAIN_API_SECRET)
sub_clients = [Client(acc["api_key"], acc["api_secret"]) for acc in SUB_ACCOUNTS]

print("✅ تم الاتصال بالحساب الرئيسي والفرعي بنجاح.")

# --------------------------------
# دالة نسخ الأوامر
# --------------------------------
def copy_order(order):
    symbol   = order["s"]     # رمز العملة
    side     = order["S"]     # BUY أو SELL
    o_type   = order["o"]     # نوع الأمر (LIMIT, MARKET...)
    quantity = order["q"]     # الكمية

    print(f"📌 نسخ أمر: {side} {quantity} {symbol} ({o_type})")

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
# WebSocket لمتابعة أوامر الحساب الرئيسي
# --------------------------------
def main_loop():
    print("🚀 بدأ البوت متابعة أوامر الحساب الرئيسي بشكل فوري...")

    twm = ThreadedWebsocketManager(api_key=MAIN_API_KEY, api_secret=MAIN_API_SECRET)
    twm.start()

    def handle_order(msg):
        if msg["e"] == "executionReport":  # رسالة تنفيذ أمر
            if msg["X"] == "NEW":  # أمر جديد
                copy_order(msg)

    twm.start_user_socket(callback=handle_order)
    twm.join()

if __name__ == "__main__":
    main_loop()
