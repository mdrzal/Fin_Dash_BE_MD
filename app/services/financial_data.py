import yfinance as yf
from typing import List, Dict
from app.services.logging_service import LoggingService

logger = LoggingService.get_logger(__name__)

def get_financial_news_for_symbol(symbol: str) -> Dict:

    logger.info(f"getting the {symbol} symbol")
    ticker = yf.Ticker(symbol)
    logger.info(f"got the {symbol} symbol")

    logger.info(f"fetching the news for the {symbol} symbol")
    news = ticker.news
    logger.info(f"got the news for the {symbol} symbol")
    
    return news

def get_recomendations_for_symbol(symbol: str) -> Dict:
    
    logger.info(f"getting the {symbol} symbol")
    ticker = yf.Ticker(symbol)
    logger.info(f"got the {symbol} symbol")

    logger.info(f"fetching the recommedations for the {symbol} symbol")
    recommendations = ticker.recommendations
    logger.info(f"got the recommedations for the {symbol} symbol")
    
    return recommendations

def get_close_prices_for_symbol(symbol: str, period: str = "1mo", interval: str = "1d") -> List[dict]:
    
    logger.info(f"Fetching close prices for {symbol}, period={period}, interval={interval}")
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period, interval=interval)
    logger.info(f"Got close prices for {symbol}")

    if hist.empty or 'Close' not in hist:
        logger.warning(f"No close price data found for {symbol}")
        return []
    
    hist = hist.reset_index()
    
    return [
        {"date": str(row["Date"])[:10], "price": float(row["Close"])}
        for _, row in hist.iterrows()
    ]

def get_pe_ratio_for_symbol(symbol: str):
    logger.info(f"Fetching P/E ratio for {symbol}")
    ticker = yf.Ticker(symbol)
    try:
        pe_ratio = ticker.info.get("trailingPE")
        logger.info(f"Got P/E ratio for {symbol}: {pe_ratio}")
        return pe_ratio
    except Exception as e:
        logger.warning(f"Failed to fetch P/E ratio for {symbol}: {e}")
        return None