# utils/yahoo_search.py

import requests

def yahoo_autocomplete_search(query):
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}&quotesCount=10&newsCount=0"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get('quotes', [])
            return [
                f"{q.get('symbol', '')} - {q.get('shortname', '')} ({q.get('exchange', '')})"
                for q in results
            ]
    except Exception:
        pass
    return []

def extract_ticker(value):
    return value.split(" - ")[0].strip() if " - " in value else value.strip()
