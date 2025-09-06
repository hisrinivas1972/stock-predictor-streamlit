def get_recent_trend(df):
    if len(df) < 14:
        return None
    last = df['y'].iloc[-7:].mean()
    prev = df['y'].iloc[-14:-7].mean()
    return "positive momentum" if last > prev else "negative momentum"
