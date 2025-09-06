import yfinance as yf

def detect_exchange(ticker):
    try:
        info = yf.Ticker(ticker).info
        return info.get('exchange', 'UNKNOWN').upper()
    except:
        return "UNKNOWN"
