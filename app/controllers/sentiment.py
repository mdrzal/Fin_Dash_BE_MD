from fastapi import HTTPException
from app.models.schemas import SentimentAnalysisResult, SentimentQueryParams
from app.services.analysis import sentiment_analysis_last24h
from app.services.logging_service import LoggingService
from app.services.cache import get_cache, set_cache

def sentiment_controller(params: SentimentQueryParams):
    logger = LoggingService.get_logger("sentiment_controller")
    cache_key = f"sentiment:{params.symbol}"
    data = get_cache(cache_key)
    if data:
        logger.info("Information for /sentiment retrieved from cache.")
        return SentimentAnalysisResult(**data)
    try:
        result = sentiment_analysis_last24h(params.symbol)
        response = SentimentAnalysisResult(mean_compound_last_24h=result["mean_compound_last_24h"], articles_last_24h=result["articles_last_24h"])
        set_cache(cache_key, response.model_dump())
        return response
    except Exception as e:
        logger.exception(f"Error in sentiment analysis: {e}")
        raise HTTPException(status_code=500, detail="Internal server error in sentiment analysis.")
