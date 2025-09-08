import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

from utils.yahoo_search import yahoo_autocomplete_search, extract_ticker
from utils.exchange_detection import detect_exchange
from utils.trend_analysis import get_recent_trend
from utils.forecasting import make_forecast

# Import news helpers from your new utility module
from utils.news_summary import get_news_headlines, summarize_news_with_gemini

st.set_page_config(page_title="📈 Stock Predictor", layout="wide")

st.markdown(
    """
    <h1 style='text-align: center;'>
        📈 <strong>WORLD-X</strong>: Multi-Asset Price Predictor
    </h1>
    <h3 style='text-align: center; font-weight: normal;'>
        Stocks | Crypto | Forex ₹ | Metals | Crude Oil
    </h3>
    <p style='text-align: center;'>🌍 One Platform for Global Markets</p>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div style='text-align: center; font-size: 1.2rem; color: red; margin-top: 10px;'>
        <strong>⚠️ Disclaimer 👇</strong>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("🔍 Inputs")
search_input = st.sidebar.text_input("Enter ticker or company name", value="AAPL")

matches = yahoo_autocomplete_search(search_input) if search_input else []
valid_ticker = False
selected_match = ""
selected_ticker = ""

if matches:
    selected_match = st.sidebar.selectbox("Select a match", matches)
    selected_ticker = extract_ticker(selected_match)
    valid_ticker = True
else:
    selected_ticker = search_input.strip().upper()
    try:
        hist_check = yf.Ticker(selected_ticker).history(period="1d")
        if not hist_check.empty:
            st.sidebar.caption("⚠️ No autocomplete match, using typed input as ticker.")
            valid_ticker = True
        else:
            st.sidebar.warning("❌ No matches found. Ticker may be invalid.")
    except:
        st.sidebar.warning("❌ Invalid input or network error.")

timeframe = st.sidebar.selectbox("Forecast Timeframe", ['1 day', '1 week', '1 month', '3 months'])

# New: API key input as password field for Google Gemini API
api_key = st.sidebar.text_input("🔑 Enter Google API Key (for News Summary)", type="password")

# Checkbox to enable news only if API key is provided
show_news = False
if api_key:
    show_news = st.sidebar.checkbox("Show News & Summary", value=True)
else:
    st.sidebar.info("Enter your Google API Key above to enable News & Summary")

predict_button = st.sidebar.button("🔮 Predict Price")

if predict_button and valid_ticker:
    try:
        stock = yf.Ticker(selected_ticker)
        company = stock.info.get("shortName", selected_ticker)
        exchange = detect_exchange(selected_ticker)

        forecast, df, currency, predicted, lower, upper = make_forecast(selected_ticker, timeframe)

        st.subheader(f"{selected_ticker} ({company})")
        st.write(f"Exchange: `{exchange}`")

        current_price = df['y'].iloc[-1]
        previous_price = df['y'].iloc[-2] if len(df) > 1 else current_price
        delta = current_price - previous_price
        pct = (delta / previous_price) * 100 if previous_price != 0 else 0

        st.metric("Current Price", f"{currency} {current_price:.2f}", f"{delta:+.2f} ({pct:+.2f}%)")

        st.success(f"📊 Predicted: {currency} {predicted:.2f}")
        st.caption(f"Confidence: {currency} {lower:.2f} - {upper:.2f}")

        trend = get_recent_trend(df)
        if trend:
            emoji = "📈" if trend == "positive momentum" else "📉"
            st.info(f"Recent **past trend**: {trend} {emoji}")
            st.caption("📌 Trend shows the past 14 days; prediction forecasts the future price.")

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df['ds'], df['y'], label="Historical", color="blue")
        ax.plot(forecast['ds'], forecast['yhat'], label="Forecast", color="orange")
        ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='orange', alpha=0.3)
        ax.axvline(df['ds'].iloc[-1], color='gray', linestyle='--', label='Today')
        ax.set_xlabel("Date")
        ax.set_ylabel(f"Price ({currency})")
        ax.set_title(f"{selected_ticker} Price Forecast")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        # News & Summary Section (only if enabled & API key provided)
        if show_news:
            st.markdown("---")
            st.header("📰 Latest News & Summary")

            try:
                headlines = get_news_headlines(selected_ticker)
                if not headlines:
                    st.warning("No recent news found for this ticker.")
                else:
                    st.subheader("Recent Headlines:")
                    for h in headlines:
                        st.write(f"• {h}")

                    st.info("🧠 Generating news summary using Gemini AI...")
                    summary = summarize_news_with_gemini(headlines, api_key)
                    st.markdown("**Summary:**")
                    st.write(summary)

            except Exception as e:
                st.error(f"❌ Error fetching or summarizing news: {e}")

    except Exception as e:
        st.error(f"❌ Error: {e}")

st.sidebar.markdown(
    """
    **Examples for Input:**  
    AAPL, RELIANCE.NS, VOD.L, 
    SAP.DE, RY.TO,  
    EURUSD=X, USDJPY=X, GBPUSD=X,  
    BTC-USD, ETH-USD, DOGE-USD,  
    GC=F, SI=F, HG=F, PL=F,  
    CL=F, CLT=F, BZT=F, BZ=F, HO=F, RB=F  
    """
)


st.markdown(
    """
    <hr>
    <div style='color: red; font-size: 1rem; max-width: 700px; margin: 20px auto; text-align: justify;'> 
        This application uses a generative AI model to produce speculative stock price predictions.  
        All information provided is for educational and demonstrative purposes only.  
        It does not constitute financial advice, and should not be used for making actual investment decisions.  
        The generated data is fictional and does not reflect real market conditions.
    </div>
    """,
    unsafe_allow_html=True
)
