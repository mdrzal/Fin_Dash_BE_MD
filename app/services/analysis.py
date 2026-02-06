from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
from app.services.logging_service import LoggingService
from app.startup.vader_startup import init_vader_sia
from app.services.financial_data import get_financial_news_for_symbol

logger = LoggingService.get_logger(__name__)

def sentiment_analysis_last24h(symbol: str) -> Dict:
    
    vader = init_vader_sia()
    news = get_financial_news_for_symbol(symbol)

    cleaned_news = []
    output_summary = []

    now = datetime.now(timezone.utc)
    one_day_ago = now - timedelta(days=1)

    for i in news:
        content = i.get("content", {})
        pubDate_str = content.get("pubDate")
        if not pubDate_str:
            continue

        pubDate = datetime.fromisoformat(pubDate_str.replace("Z", "+00:00"))
        if pubDate < one_day_ago:
            continue

        summary = content.get("summary", "")
        if summary:
            scores = vader.polarity_scores(summary)
        else:
            scores = {"neg": 0, "neu": 1, "pos": 0, "compound": 0}

        output_summary.append({
            "title": content.get("title", "No title"),
            "summary": summary,
            "previewUrl": content.get("canonicalUrl", ""),
            "vader_compound": scores["compound"]
        })

    mean_compound = (
        sum(item["vader_compound"] for item in output_summary) / len(output_summary)
        if output_summary
        else 0.0
    )

    return {
        "mean_compound_last_24h": mean_compound,
        "articles_last_24h": output_summary,
    }

# --- Core Metrics Functions ---
def calculate_return(prices: List[float]) -> Optional[float]:
    if not prices or len(prices) < 2:
        return None
    return (prices[-1] - prices[0]) / prices[0]

def calculate_volatility(prices: List[float]) -> Optional[float]:
    if not prices or len(prices) < 2:
        return None
    returns = np.diff(prices) / prices[:-1]
    return float(np.std(returns))

def calculate_rsi(prices: List[float], period: int = 14) -> Optional[float]:
    if not prices or len(prices) < period + 1:
        return None
    deltas = np.diff(prices)
    seed = deltas[:period]
    up = seed[seed > 0].sum() / period
    down = -seed[seed < 0].sum() / period
    if down == 0:
        return 100.0
    rs = up / down
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return float(rsi)

def calculate_moving_average(prices: List[float], window: int = 20) -> Optional[List[float]]:
    if not prices or len(prices) < window:
        return None
    return list(pd.Series(prices).rolling(window=window).mean().dropna())
