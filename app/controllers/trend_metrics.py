from fastapi import HTTPException
from app.models.schemas import (
    TrendMetricsQueryParams, TrendMetricsResponse
)
from app.helpers.guards import validate_symbol, validate_interval
from app.services.financial_data import get_close_prices_for_symbol
from app.services.analysis import calculate_moving_average
from app.services.logging_service import LoggingService
from app.services.cache import get_cache, set_cache


def trend_metrics_controller(params: TrendMetricsQueryParams):
    logger = LoggingService.get_logger("trend_metrics_controller")
    validate_symbol(params.symbol)
    cache_key = f"trend:{params.symbol}"
    data = get_cache(cache_key)
    if data:
        logger.info("Information for /trend-metrics retrieved from cache.")
        return TrendMetricsResponse(**data)
    try:
        # Always fetch 21 days for 20-day trend metrics
        prices_dict = get_close_prices_for_symbol(params.symbol, "21d", "1d")
        if not prices_dict or len(prices_dict) < 21:
            raise HTTPException(status_code=404, detail="Not enough price data found for trend metrics.")

        prices = [p["price"] for p in prices_dict]
        current_price = prices[-1]
        price_20_days_ago = prices[-21]
        sma_20_list = calculate_moving_average(prices, 20)
        sma_20 = sma_20_list[-1] if sma_20_list else None
        sma_gap = current_price - sma_20 if sma_20 is not None else None
        momentum_20d = current_price - price_20_days_ago if price_20_days_ago is not None else None

        response = TrendMetricsResponse(
            momentum_20d=momentum_20d,
            sma_gap=sma_gap
        )
        set_cache(cache_key, response.model_dump())
        return response
    except Exception as e:
        logger.exception(f"Error in trend metrics calculation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error in trend metrics calculation.")
