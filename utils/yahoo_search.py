import requests

def yahoo_autocomplete_search(query):
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}&quotesCount=10&newsCount=0"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            quotes = res.json().get("quotes", [])
            return [f"{q.get('symbol')} - {q.get('shortname')} ({q.get('exchange')})" for q in quotes]
    except:
        pass
    return []

def extract_ticker(value):
    return value.split(" - ")[0].strip() if " - " in value else value.strip()
