from textblob import TextBlob

def analyze_sentiment(articles):
    """
    Analyzes sentiment for a list of articles and returns an overall sentiment score.
    """
    total_polarity = 0
    total_subjectivity = 0
    valid_articles = 0  # ✅ Track how many articles have valid content

    if not isinstance(articles, list):  # ✅ Ensure it's a list
        return "No news articles available for sentiment analysis."

    for article in articles:
        if isinstance(article, dict):  
            content = article.get("content") or article.get("title", "")  # ✅ Use title if content is missing
        elif isinstance(article, str):  
            content = article  # ✅ If it's a string, use it directly
        else:
            continue  # Skip invalid articles
        
        if not content.strip():  # ✅ Skip empty strings
            continue  

        analysis = TextBlob(content)
        total_polarity += analysis.sentiment.polarity
        total_subjectivity += analysis.sentiment.subjectivity
        valid_articles += 1

    # ✅ Ensure division by zero doesn't happen
    if valid_articles == 0:
        return "No valid articles found for sentiment analysis."

    # Compute averages
    avg_polarity = total_polarity / valid_articles
    avg_subjectivity = total_subjectivity / valid_articles

    # Determine overall sentiment
    if avg_polarity > 0.1:
        sentiment_result = "Positive"
    elif avg_polarity < -0.1:
        sentiment_result = "Negative"
    else:
        sentiment_result = "Neutral"

    return (
        f"Overall Sentiment: {sentiment_result}\n"
        f"Polarity Score: {avg_polarity:.2f}\n"
        f"Subjectivity Score: {avg_subjectivity:.2f}\n"
        f"Analyzed {valid_articles} article(s)"
    )
