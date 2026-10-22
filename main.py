from fastapi import FastAPI, Request
import requests
import uvicorn
import os

app = FastAPI()

# تذكر وضع بياناتك الحقيقية هنا بدلاً من الكلمات الافتراضية
TELEGRAM_TOKEN = "8805409524:AAHISPXyj8Vtek5jIYeWs1DxH2EfiyjcG0w"
CHAT_ID = "8099576587"

def send_telegram(message):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

@app.post("/webhook")
async def tradingview_webhook(request: Request):
    try:
        data = await request.json()
        pair = data.get("pair", "UNKNOWN")
        action = data.get("action", "HOLD")
        price = data.get("price", "0.0")
        
        emoji = "🟢 CALL / BUY" if action == "BUY" else "🔴 PUT / SELL"
        
        message = (
            f"🚨 **إشارة تداول فوري (Pocket Option)** 🚨\n\n"
            f"📊 **الزوج:** {pair}\n"
            f"⏳ **المدة:** 1 MIN\n"
            f"⚡ **الإجراء:** {emoji}\n"
            f"💵 **سعر الدخول:** {price}\n\n"
            f"⚠️ *تأكيد الاستراتيجية: (EMA 200 + RSI + Stochastic + MACD)*"
        )
        
        send_telegram(message)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
