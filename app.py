import requests
import pandas as pd
import talib
from telegram.ext import Updater, CommandHandler
import schedule
import time

# === API ve Telegram Ayarları ===
API_KEY = 'ct6plq9r01qmbqosf810ct6plq9r01qmbqosf81g'
TELEGRAM_BOT_TOKEN = '8123413927:AAF2MXNAsIqHDtqZddBS3tnZDDK0L7Fgw4g'
SYMBOLS = ['GARAN.IS', 'AKBNK.IS', 'THYAO.IS']  # İzlemek istediğiniz hisseler
print(talib.get_functions())

# Telegram bot mesaj fonksiyonu
def send_telegram_message(message):
    bot = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    bot.bot.send_message(chat_id="KULLANICI_CHAT_ID", text=message)

# === Hisse Verisi Çekme Fonksiyonu ===
def fetch_stock_data(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['c'], data['h'], data['l']  # Güncel fiyat, yüksek, düşük
    else:
        return None

# === Teknik Analiz Fonksiyonu ===
def analyze_stock(symbol):
    # Örnek veri (gerçekte geçmiş fiyatlar çekilmeli)
    prices = {
        'close': [10, 12, 11, 13, 12, 14, 15, 16, 15, 14]
    }
    df = pd.DataFrame(prices)

    # RSI hesapla
    df['RSI'] = talib.RSI(df['close'], timeperiod=14)

    # Sinyal oluştur
    if df['RSI'].iloc[-1] < 30:
        return f"{symbol} için LONG sinyali!"
    elif df['RSI'].iloc[-1] > 70:
        return f"{symbol} için SHORT sinyali!"
    else:
        return f"{symbol} için HOLD sinyali."

# === Ana İşlem Döngüsü ===
def check_and_send_signals():
    for symbol in SYMBOLS:
        try:
            current_price, high, low = fetch_stock_data(symbol)
            analysis = analyze_stock(symbol)
            message = f"{symbol}\nFiyat: {current_price}\n{analysis}"
            send_telegram_message(message)
        except Exception as e:
            print(f"Error with {symbol}: {e}")

# === Sürekli Çalıştırma ===
def run_scheduler():
    schedule.every(1).hour.do(check_and_send_signals)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    print("Hisse Sinyal Botu Başlatıldı...")
    run_scheduler()
