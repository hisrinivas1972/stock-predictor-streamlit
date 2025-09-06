import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from prophet import Prophet

from utils.yahoo_search import yahoo_autocomplete_search, extract_ticker
from utils.exchange_detection import detect_exchange
from utils.trend_analysis import get_recent_trend
from utils.forecasting import make_forecast

st.set_page_config(page_title="Stock Predictor", layout="centered")
st.title("📈 Stock / Crypto / Forex Predictor")

search_input = st.text_input("Enter ticker or company name")
selected_match = ""
if search_input:
    matches = yahoo_autocomplete_search(search_input)
    if matches:
        selected_match = st.selectbox("Select match", matches)
    else:
        st.warning("No matches found.")
        selected_match = search_input

timeframe = st.selectbox("Forecast Timeframe", ['1 day', '1 week', '1 month', '3 months'])
if st.button("🔮 Predict Price") and selected_match:
    ticker = extract_ticker(selected_match)
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        if hist.empty:
            st.error("No data found.")
        else:
            forecast, df, currency, predicted, lower, upper = make_forecast(ticker, timeframe)
            st.metric("Current Price", f"{currency} {df['y'].iloc[-1]:.2f}")
            st.success(f"Predicted: {currency} {predicted:.2f} ({lower:.2f} - {upper:.2f})")
            trend = get_recent_trend(df)
            if trend:
                st.info(f"Recent momentum: {trend}")

            fig, ax = plt.subplots(figsize=(10,5))
            ax.plot(df['ds'], df['y'], label="History")
            ax.plot(forecast['ds'], forecast['yhat'], label="Forecast")
            ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], alpha=0.3)
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Error: {e}")
