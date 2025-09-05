# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import time

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from binance.client import Client
    from binance.enums import *
    from binance import ThreadedWebsocketManager
except ImportError:
    install("python-binance")
    from binance.client import Client
    from binance.enums import *
    from binance import ThreadedWebsocketManager

# قراءة المفاتيح من Secrets
MAIN_API_KEY    = os.getenv("MAIN_API_KEY")
MAIN_API_SECRET = os.getenv("MAIN_API_SECRET")

if not MAIN_API_KEY or not MAIN_API_SECRET:
    raise ValueError("⚠️ تأكد من إضافة MAIN_API_KEY و MAIN_API_SECRET في أداة Secrets.")

# الحسابات الفرعية
SUB_ACCOUNTS = []
for i in range(1, 16):
    key = os.getenv(f"SUB{i}_API_KEY")
    secret = os.getenv(f"SUB{i}_API_SECRET")
    if key and secret:
        SUB_ACCOUNTS.append({"api_key": key, "api_secret": secret})

main_client = Client(MAIN_API_KEY, MAIN_API_SECRET)
sub_clients = [Client(acc["api_key"], acc["api_secret"]) for acc in SUB_ACCOUNTS]

print("✅ تم الاتصال بالحساب الرئيسي والفرعي بنجاح.")

def copy_order(order):
    symbol   = order["s"]
    side     = order["S"]
    o_type   = order["o"]
    quantity = order["q"]
    price    = order.get("p")

    print(f"📌 نسخ أمر: {side} {quantity} {symbol} ({o_type})")

    for i, client in enumerate(sub_clients, start=1):
        try:
            if o_type == "MARKET":
                client.create_order(
                    symbol=symbol,
                    side=side,
                    type=o_type,
                    quantity=quantity
                )
            elif o_type == "LIMIT":
                client.create_order(
                    symbol=symbol,
                    side=side,
                    type=o_type,
                    quantity=quantity,
                    price=price,
                    timeInForce="GTC"
                )
            print(f"   ✅ نُفِّذ في الحساب الفرعي {i}")
        except Exception as e:
            print(f"   ❌ خطأ في الحساب الفرعي {i}: {e}")

def main_loop():
    print("🚀 بدأ البوت متابعة أوامر الحساب الرئيسي بشكل فوري...")

    twm = ThreadedWebsocketManager(api_key=MAIN_API_KEY, api_secret=MAIN_API_SECRET)
    twm.start()

    def handle_order(msg):
        if msg["e"] == "executionReport" and msg["X"] == "NEW":
            copy_order(msg)

    twm.start_user_socket(callback=handle_order)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 تم إيقاف البوت.")
        twm.stop()

if __name__ == "__main__":
    main_loop()
