from fastapi import HTTPException
from app.models.schemas import (
    CoreMetricsQueryParams, CoreMetricsResponse
)
from app.helpers.guards import validate_symbol, validate_interval
from app.services.financial_data import get_close_prices_for_symbol, get_pe_ratio_for_symbol
from app.services.analysis import calculate_return, calculate_volatility, calculate_rsi
from app.services.logging_service import LoggingService
from app.services.cache import get_cache, set_cache


def core_metrics_controller(params: CoreMetricsQueryParams):
    logger = LoggingService.get_logger("core_metrics_controller")
    validate_symbol(params.symbol)
    validate_interval(params.interval)
    cache_key = f"coremetrics:{params.symbol}:{params.period_months}:{params.interval}:{params.rsi_period}"
    data = get_cache(cache_key)
    if data:
        logger.info("Information for /core-metrics retrieved from cache.")
        return CoreMetricsResponse(**data)
    try:
        period = f"{params.period_months}mo"
        prices_dict = get_close_prices_for_symbol(params.symbol, period, params.interval)
        if not prices_dict:
            raise HTTPException(status_code=404, detail="No price data found for symbol.")

        prices = [p["price"] for p in prices_dict]

        prices_1m_dict = get_close_prices_for_symbol(params.symbol, "1mo", params.interval)
        prices_3m_dict = get_close_prices_for_symbol(params.symbol, "3mo", params.interval)
        prices_1m = [p["price"] for p in prices_1m_dict] if prices_1m_dict else None
        prices_3m = [p["price"] for p in prices_3m_dict] if prices_3m_dict else None

        return_1m = calculate_return(prices_1m) if prices_1m else None
        return_3m = calculate_return(prices_3m) if prices_3m else None

        pe_ratio = get_pe_ratio_for_symbol(params.symbol)

        # For RSI, fetch prices for the last rsi_period + 1 days
        rsi_days = params.rsi_period + 1
        rsi_prices_dict = get_close_prices_for_symbol(params.symbol, f"{rsi_days}d", "1d")
        rsi_prices = [p["price"] for p in rsi_prices_dict] if rsi_prices_dict else prices

        response = CoreMetricsResponse(
            return_=calculate_return(prices),
            volatility=calculate_volatility(prices),
            rsi=calculate_rsi(rsi_prices, params.rsi_period),
            return_1m=return_1m,
            return_3m=return_3m,
            pe_ratio=pe_ratio
        )
        set_cache(cache_key, response.model_dump())
        return response
    except Exception as e:
        logger.exception(f"Error in core metrics calculation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error in core metrics calculation.")
