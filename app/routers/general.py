from fastapi import APIRouter, Depends
from app.models.schemas import (
    CompanyInfoQueryParams, SentimentQueryParams, RecommendationsQueryParams, CoreMetricsQueryParams,
    TrendMetricsQueryParams, CorrelationMetricsQueryParams, DrawdownMetricsQueryParams,
    CoreMetricsResponse, TrendMetricsResponse, CorrelationMetricsResponse, DrawdownMetricsResponse,
    MovingAverageQueryParams, MovingAverageResponse, PricesResponse, PricesQueryParams
)
from app.controllers.prices import prices_controller
from app.controllers.sentiment import sentiment_controller
from app.controllers.core_metrics import core_metrics_controller
from app.controllers.moving_average import moving_average_controller
from app.controllers.trend_metrics import trend_metrics_controller
from app.controllers.correlation_metrics import correlation_metrics_controller
from app.controllers.drawdown_metrics import drawdown_metrics_controller
from app.controllers.recommendations import recommendations_controller
from app.controllers.available_tickers import available_tickers_controller
from app.controllers.company_about import get_company_about
from app.models.schemas import AvailableTickersQueryParams
from app.controllers.parameter_options import parameter_options_controller

router = APIRouter()

@router.get("/valid-parameter-options")
async def get_valid_parameter_options():
    return parameter_options_controller()

# --- Regular Prices ---
@router.get("/prices", response_model=PricesResponse)
async def get_prices(params: PricesQueryParams = Depends()):
    return prices_controller(params)

# --- Sentiment Analysis ---
@router.get("/sentiment")
async def sentiment(params: SentimentQueryParams = Depends()):
    return sentiment_controller(params)

# --- Unified Core Metrics Endpoint ---
@router.get("/core-metrics", response_model=CoreMetricsResponse)
async def get_core_metrics(params: CoreMetricsQueryParams = Depends()):
    return core_metrics_controller(params)

# --- Moving Average Endpoint ---
@router.get("/moving-average", response_model=MovingAverageResponse)
async def get_moving_average(params: MovingAverageQueryParams = Depends()):
    return moving_average_controller(params)
    
# --- Trend Metrics Endpoint ---
@router.get("/trend-metrics", response_model=TrendMetricsResponse)
async def get_trend_metrics(params: TrendMetricsQueryParams = Depends()):
    return trend_metrics_controller(params)
    
# --- Correlation & Beta Metrics Endpoint ---
@router.get("/correlation-metrics", response_model=CorrelationMetricsResponse)
async def get_correlation_metrics(params: CorrelationMetricsQueryParams = Depends()):
    return correlation_metrics_controller(params)

    
# --- Drawdown Analysis Endpoint ---
@router.get("/drawdown-metrics", response_model=DrawdownMetricsResponse)
async def get_drawdown_metrics(params: DrawdownMetricsQueryParams = Depends()):
    return drawdown_metrics_controller(params)

# --- Available Tickers ---
@router.get("/available-tickers")
async def get_available_tickers(params: AvailableTickersQueryParams = Depends()):
    return available_tickers_controller(params)
    
# --- Recommendations  ---
@router.get("/recommendations")
async def recommendations(params: RecommendationsQueryParams = Depends()):
    return recommendations_controller(params)

# --- Company About Endpoint ---
@router.get("/company-about")
async def company_about(params: CompanyInfoQueryParams = Depends()):
    return get_company_about(params)