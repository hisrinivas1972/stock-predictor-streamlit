import feedparser
import google.generativeai as genai
import urllib.parse

def get_news_headlines(company_name, max_items=5):
    """
    Fetches recent news headlines related to the company/ticker.
    Handles special commodity tickers and URL encoding.
    """
    commodities = {
        "GC=F": "Gold",
        "SI=F": "Silver",
        "HG=F": "Copper",
        "PL=F": "Platinum",
        "CL=F": "Crude Oil",
        "BRN=F": "Brent Oil",
        "HO=F": "Heating Oil",
        "RB=F": "RBOB Gasoline"        # add more commodities if needed
    }
    
    # Use friendly keyword for commodities to avoid ambiguous news
    if company_name.upper() in commodities:
        query = commodities[company_name.upper()].replace(' ', '+')
    else:
        # URL encode for safe query string (handle = sign and others)
        query = urllib.parse.quote(company_name)
    
    rss_url = f"https://news.google.com/rss/search?q={query}+stock"
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
