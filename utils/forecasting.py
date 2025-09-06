# utils/forecasting.py

from prophet import Prophet
import yfinance as yf

def make_forecast(ticker, timeframe):
    stock = yf.Ticker(ticker)
    info = stock.info
    currency = info.get("currency", "USD")

    df = stock.history(period="1y")[["Close"]].reset_index()
    df.columns = ["ds", "y"]
    df['ds'] = df['ds'].dt.tz_localize(None)  # ✅ Fix timezone issue

    model = Prophet(daily_seasonality=True)
    model.fit(df)

    periods_map = {'1 day': 1, '1 week': 7, '1 month': 30, '3 months': 90}
    future = model.make_future_dataframe(periods=periods_map[timeframe])
    forecast = model.predict(future)

    predicted = forecast.iloc[-1]['yhat']
    lower = forecast.iloc[-1]['yhat_lower']
    upper = forecast.iloc[-1]['yhat_upper']

    return forecast, df, currency, predicted, lower, upper
