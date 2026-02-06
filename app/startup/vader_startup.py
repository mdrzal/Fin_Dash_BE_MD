from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from app.services.logging_service import LoggingService

logger = LoggingService.get_logger(__name__)
vader_sentiment_intensity_analyzer = None

def init_vader_sia():
    global vader_sentiment_intensity_analyzer
    if vader_sentiment_intensity_analyzer is None:
        nltk.download("vader_lexicon", quiet=True)
        vader_sentiment_intensity_analyzer = SentimentIntensityAnalyzer()
        logger.info("Using default NLTK VADER lexicon")
    return vader_sentiment_intensity_analyzer
