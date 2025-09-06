import feedparser
import google.generativeai as genai

def get_news_headlines(company_name, max_items=5):
    """
    Fetches recent news headlines related to the company/ticker.
    """
    rss_url = f"https://news.google.com/rss/search?q={company_name.replace(' ', '+')}+stock"
    feed = feedparser.parse(rss_url)
    headlines = [entry['title'] for entry in feed.entries[:max_items]]
    return headlines

def summarize_news_with_gemini(headlines, api_key):
    """
    Uses Google Gemini AI to generate a summary of given headlines.
    Dynamically configures the API key on each call.
    """
    genai.configure(api_key=api_key)
    prompt = f"Summarize the following recent news headlines for investors:\n\n{chr(10).join(headlines)}"
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()
