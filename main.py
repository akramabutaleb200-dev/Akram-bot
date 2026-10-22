import time
import requests
import pandas as pd

# إعدادات البوت وقناتك (تأكد من كتابتها بدقة داخل علامات التنصيص)
TELEGRAM_TOKEN = "8805409524:AAHISPXyj8Vtek5jIYeWs1DxH2EfiyjcG0w"
CHAT_ID = "8099576587"

def send_telegram(message):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try: requests.post(url, json=payload)
    except Exception as e: print(f"Error: {e}")

def get_live_data():
    # جلب أسعار دقيقة حية ومجانية لزوج EUR/USD عبر سيرفر عام
    try:
        url = "https://binance.com"
        data = requests.get(url).json()
        df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'qav', 'num_trades', 'taker_base', 'taker_quote', 'ignore'])
        return df['close'].astype(float)
    except: return None

def calculate_signals():
    print("البوت يعمل الآن ويراقب الأسواق كل دقيقة...")
    send_telegram("🚀 **تم تشغيل بوت الإشارات الذكي مباشرة عبر GitHub بنجاح!**")
    
    while True:
        prices = get_live_data()
        if prices is not None and len(prices) > 200:
            # حساب المؤشرات ببساطة شديدة وبدون تعقيد
            current_price = prices.iloc[-1]
            ema200 = prices.ewm(span=200, adjust=False).mean().iloc[-1]
            
            # حساب تقريبي وسريع لمؤشر RSI على فريم الدقيقة
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean().iloc[-1]
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean().iloc[-1]
            rs = gain / (loss if loss != 0 else 1)
            rsi = 100 - (100 / (1 + rs))

            # شروط الاستراتيجية (EMA 200 + RSI) بدقة دقيقة واحدة
            if current_price > ema200 and rsi < 30:
                msg = f"🚨 **إشارة Pocket Option** 🚨\n\n📊 الزوج: EUR/USD\n⏳ المدة: 1 MIN\n⚡ الإجراء: 🟢 **شراء CALL / BUY**\n💵 السعر: {current_price}"
                send_telegram(msg)
                time.sleep(60) # انتظر دقيقة كاملة قبل الفحص التالي لمنع تكرار الإشارة
                
            elif current_price < ema200 and rsi > 70:
                msg = f"🚨 **إشارة Pocket Option** 🚨\n\n📊 الزوج: EUR/USD\n⏳ المدة: 1 MIN\n⚡ الإجراء: 🔴 **بيع PUT / SELL**\n💵 السعر: {current_price}"
                send_telegram(msg)
                time.sleep(60)

        time.sleep(10) # فحص تحديث السوق كل 10 ثوانٍ

if __name__ == "__main__":
    calculate_signals()
