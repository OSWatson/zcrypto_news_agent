from textblob import TextBlob
import numpy as np


def analyze_sentiment(articles):
    """
    Analyzes sentiment for a list of articles and returns an overall sentiment score.
    
    Args:
        articles: List of article texts or list of dictionaries containing article data
    
    Returns:
        str: Formatted string containing sentiment analysis results
    """
    total_polarity = 0
    total_subjectivity = 0
    polarities = []
    valid_articles = 0

    # Handle different input types
    if isinstance(articles, str):
        articles = [articles]
    
    for article in articles:
        # Extract text from article (handle both string and dict inputs)
        if isinstance(article, dict):
            title = article.get('title', '') or ''
            content = article.get('content', '') or ''
            full_text = f"{title} {content}"
        else:
            full_text = str(article)
        
        if not full_text.strip():
            continue

        # Perform sentiment analysis
        analysis = TextBlob(full_text)
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity
        
        total_polarity += polarity
        total_subjectivity += subjectivity
        polarities.append(polarity)
        valid_articles += 1

    if valid_articles == 0:
        print("No valid articles found for sentiment analysis.")  # Debugging line
        return "No valid articles found for sentiment analysis."

    # Calculate metrics
    avg_polarity = total_polarity / valid_articles
    avg_subjectivity = total_subjectivity / valid_articles
    std_polarity = np.std(polarities) if len(polarities) > 1 else 0

    # Determine overall sentiment
    if avg_polarity > 0.1:
        sentiment_result = "Positive"
    elif avg_polarity < -0.1:
        sentiment_result = "Negative"
    else:
        sentiment_result = "Neutral"

    # Add confidence level based on standard deviation
    confidence = "High" if std_polarity < 0.3 else "Medium" if std_polarity < 0.5 else "Low"

    return (
        f"Overall Sentiment: {sentiment_result}\n"
        f"Polarity Score: {avg_polarity:.2f}\n"
        f"Subjectivity Score: {avg_subjectivity:.2f}\n"
        f"Confidence: {confidence}\n"
        f"Analyzed: {valid_articles} article(s)"
    )
