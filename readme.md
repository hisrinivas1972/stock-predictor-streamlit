# Multi-Asset Price Prediction App

This is a Streamlit-based web application that provides AI-powered price predictions for multiple asset classes including stocks, cryptocurrencies, forex, and commodities. The app offers multi-timeframe forecasts (1 day, 1 week, 1 month, 3 months) along with confidence intervals and trend insights.

---

## Features

- **Multi-Timeframe Price Predictions:**  
  Forecast price movements for stocks, crypto, forex, and commodities.

- **Global Market Support:**  
  Works with a wide range of tickers such as AAPL, BTC-USD, EURUSD=X, Brent Crude Oil (BZ=F), and more.

- **Ticker-Specific News Summaries:**  
  By providing a Google API Key, users can unlock AI-generated news summaries relevant to the specific ticker for deeper market insights. This feature leverages Google News API and Gemini AI for summarization.

- **User-Friendly Interface:**  
  Simple input for ticker, forecast timeframe, and optional Google API key.

---

## How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/hisrinivas1972/stock-predictor-streamlit.git
   cd stock-price-streamlit
   
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the Streamlit app:

bash
Copy code
streamlit run app.py
In the app:

Enter the ticker symbol (e.g., AAPL, BTC-USD, BZ=F).

Select the forecast timeframe (1 day, 1 week, 1 month, 3 months).

(Optional) Enter your Google API Key to get ticker-specific news summaries.

Disclaimer
This application uses AI-generated models and third-party data to provide speculative price predictions and news summaries for educational and demonstrative purposes only. It does not constitute financial advice or recommendations. Predictions may not reflect actual market outcomes. Users should perform their own due diligence and consult financial professionals before making any investment decisions.

Tech Stack
Python

Streamlit

Yahoo Finance API (or equivalent)

Google News API (user-provided key)

Gemini AI for news summarization

Demo
Try the live app here:
https://stock-predictor-app-cqwmt2o3nwmpti92u8n7j2.streamlit.app/

Contributions
Feel free to fork and submit pull requests. Open to suggestions and improvements!

License
MIT License

Made with ❤️ by hisrinivas1972
