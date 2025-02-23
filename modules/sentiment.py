from textblob import TextBlob

def analyze_sentiment(text):
    if not text:  # Handle None or empty text
        return "Neutral"
    
    score = TextBlob(text).sentiment.polarity
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"
