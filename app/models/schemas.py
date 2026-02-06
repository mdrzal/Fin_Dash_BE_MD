from typing import Optional
from fastapi import Query
from pydantic import BaseModel
from typing import List
from enum import Enum

class IntervalEnum(str, Enum):
    day = "1d"
    hour = "1h"
    week = "1wk"

class MAWindowEnum(int, Enum):
    short = 10
    standard = 20
    long = 50
    very_long = 200

MAX_PERIOD_MONTHS = 60
MIN_PERIOD_MONTHS = 1

class SentimentAnalysisResult(BaseModel):
    mean_compound_last_24h: float
    articles_last_24h: List[dict]

class SymbolRequestClass(BaseModel):
    symbol: str

class SentimentQueryParams(SymbolRequestClass):
    pass

class RecommendationsQueryParams(SymbolRequestClass):
    pass

class PricePoint(BaseModel):
    price: float
    date: str
    
class AvailableTicker(BaseModel):
    symbol: str
    name: str

class PricesQueryParams(BaseModel):
    symbol: str = Query(..., description="Stock ticker symbol (e.g., 'AAPL').")
    period_months: int = Query(1, ge=MIN_PERIOD_MONTHS, le=MAX_PERIOD_MONTHS, description=f"Number of months of historical data to use (min {MIN_PERIOD_MONTHS}, max {MAX_PERIOD_MONTHS}).")
    interval: IntervalEnum = Query(IntervalEnum.day, description="Data interval for price sampling. Options: '1d' (daily), '1h' (hourly), '1wk' (weekly).")

# --- Query Schemas ---
class DrawdownMetricsQueryParams(BaseModel):
    symbol: str = Query(..., description="Stock ticker symbol (e.g., 'AAPL').")
    period_months: int = Query(12, ge=MIN_PERIOD_MONTHS, le=MAX_PERIOD_MONTHS, description=f"Number of months of historical data to use (min {MIN_PERIOD_MONTHS}, max {MAX_PERIOD_MONTHS}).")
    interval: IntervalEnum = Query(IntervalEnum.day, description="Data interval for price sampling. Options: '1d' (daily), '1wk' (weekly).")
    
class CoreMetricsQueryParams(BaseModel):
    symbol: str = Query(..., description="Stock ticker symbol (e.g., 'AAPL' for Apple Inc.).")
    period_months: int = Query(1, ge=MIN_PERIOD_MONTHS, le=MAX_PERIOD_MONTHS, description=f"Number of months of historical data to use for main metrics (min {MIN_PERIOD_MONTHS}, max {MAX_PERIOD_MONTHS}).")
    interval: IntervalEnum = Query(IntervalEnum.day, description="Data interval for price sampling. Options: '1d' (daily), '1h' (hourly), '1wk' (weekly).")
    rsi_period: int = Query(14, description="Number of periods (days) to use for RSI calculation. Standard is 14.")

class TrendMetricsQueryParams(BaseModel):
    symbol: str = Query(..., description="Stock ticker symbol (e.g., 'AAPL' for Apple Inc.).")

class CorrelationMetricsQueryParams(BaseModel):
    symbol: str = Query(..., description="Stock ticker symbol (e.g., 'AAPL').")
    benchmark: str = Query("^GSPC", description="Benchmark ticker symbol (e.g., '^GSPC' for S&P 500).")
    period_months: int = Query(6, ge=MIN_PERIOD_MONTHS, le=MAX_PERIOD_MONTHS, description=f"Number of months of historical data to use (min {MIN_PERIOD_MONTHS}, max {MAX_PERIOD_MONTHS}).")
    interval: IntervalEnum = Query(IntervalEnum.day, description="Data interval for price sampling. Options: '1d' (daily), '1h' (hourly), '1wk' (weekly).")


class MovingAverageQueryParams(BaseModel):
    symbol: str = Query(..., description="Stock ticker symbol (e.g., 'AAPL').")
    period_months: int = Query(1, ge=MIN_PERIOD_MONTHS, le=MAX_PERIOD_MONTHS, description=f"Number of months of historical data to use (min {MIN_PERIOD_MONTHS}, max {MAX_PERIOD_MONTHS}).")
    interval: IntervalEnum = Query(IntervalEnum.day, description="Data interval for price sampling. Options: '1d' (daily), '1h' (hourly), '1wk' (weekly).")
    window: MAWindowEnum = Query(MAWindowEnum.standard, description="Window size for moving average calculation. Options: 10, 20, 50, 200.")


# --- Company Info Query Schema ---
class CompanyInfoQueryParams(SymbolRequestClass):
    pass

# --- Company Info Response Schema ---
class CompanyInfoResponse(BaseModel):
    symbol: str
    name: str
    sector: str = None
    industry: str = None
    website: str = None
    description: str = None
    market_cap: float = None

class AvailableTickersQueryParams(BaseModel):
    starts_with: Optional[str] = Query(None, min_length=1, max_length=5, description="Filter tickers by initial letters")

# --- Response Models ---
class CoreMetricsResponse(BaseModel):
    return_: Optional[float]
    volatility: Optional[float]
    rsi: Optional[float]
    return_1m: Optional[float]
    return_3m: Optional[float]
    pe_ratio: Optional[float]

class MovingAveragePoint(BaseModel):
    price: float
    date: str

class MovingAverageResponse(BaseModel):
    moving_average: Optional[list[MovingAveragePoint]]

class TrendMetricsResponse(BaseModel):
    momentum_20d: Optional[float]
    sma_gap: Optional[float]

class CorrelationMetricsResponse(BaseModel):
    correlation: Optional[float]
    beta: Optional[float]


class DrawdownMetricsResponse(BaseModel):
    max_drawdown_pct: Optional[float]
    recovery_days: Optional[int]
    
class PricesResponse(BaseModel):
    prices: list[PricePoint]

class AvailableTickersResponse(BaseModel):
    tickers: list[AvailableTicker]