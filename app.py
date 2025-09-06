# app.py

import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
from utils.yahoo_search import yahoo_autocomplete_search, extract_ticker
from utils.exchange_detection import detect_exchange
from utils.trend_analysis import get_recent_trend
from utils.forecasting import make_forecast

st.set_page_config(page_title="📈 Stock Predictor", layout="centered")

# ------------------------
# Sidebar Input Section
# ------------------------
st.sidebar.title("🔍 Inputs")

search_input = st.sidebar.text_input("Enter ticker or company name", value="AAPL")
selected_match = ""

if search_input:
    matches = yahoo_autocomplete_search(search_input)
    if matches:
        selected_match = st.sidebar.selectbox("Select a match", matches)
    else:
        st.sidebar.warning("No matches found.")
        selected_match = search_input

timeframe = st.sidebar.selectbox("Forecast Timeframe", ['1 day', '1 week', '1 month', '3 months'])
predict_button = st.sidebar.button("🔮 Predict Price")

# ------------------------
# Main App Section
# ------------------------
st.title("📈 Stock / Crypto / Forex Predictor")

if predict_button and selected_match:
    ticker = extract_ticker(selected_match)
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")

        if hist.empty:
            st.error("No historical data found.")
        else:
            forecast, df, currency, predicted, lower, upper = make_forecast(ticker, timeframe)
            company = stock.info.get("shortName", ticker)

            st.subheader(f"{ticker} ({company})")
            st.write(f"Exchange: `{detect_exchange(ticker)}`")

            # Current price metrics
            current_price = df['y'].iloc[-1]
            previous_price = df['y'].iloc[-2] if len(df) > 1 else current_price
            delta = current_price - previous_price
            pct = (delta / previous_price) * 100 if previous_price != 0 else 0
            st.metric("Current Price", f"{currency} {current_price:.2f}", f"{delta:+.2f} ({pct:+.2f}%)")

            # Prediction
            st.success(f"📊 Predicted: {currency} {predicted:.2f}")
            st.caption(f"Confidence: {currency} {lower:.2f} - {upper:.2f}")

            # Momentum
            trend = get_recent_trend(df)
            if trend:
                emoji = "📈" if trend == "positive momentum" else "📉"
                st.info(f"Recent trend: **{trend}** {emoji}")

            # Plot
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(df['ds'], df['y'], label="Historical", color="blue")
            ax.plot(forecast['ds'], forecast['yhat'], label="Forecast", color="orange")
            ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='orange', alpha=0.3)
            ax.axvline(df['ds'].iloc[-1], color='gray', linestyle='--', label='Today')
            ax.set_xlabel("Date")
            ax.set_ylabel(f"Price ({currency})")
            ax.set_title(f"{ticker} Price Forecast")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error: {e}")
