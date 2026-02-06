from fastapi import HTTPException
from app.models.schemas import (
    CorrelationMetricsQueryParams, CorrelationMetricsResponse
)
from app.helpers.guards import validate_interval
from app.services.financial_data import get_close_prices_for_symbol
from app.services.logging_service import LoggingService
from app.services.cache import get_cache, set_cache
import numpy as np

def correlation_metrics_controller(params: CorrelationMetricsQueryParams):
    logger = LoggingService.get_logger("correlation_metrics_controller")
    validate_interval(params.interval)
    if params.benchmark != "^GSPC":
        raise HTTPException(status_code=422, detail="Only S&P 500 (^GSPC) is allowed as benchmark.")
    cache_key = f"corr:{params.symbol}:{params.benchmark}:{params.period_months}:{params.interval}"
    data = get_cache(cache_key)
    if data:
        logger.info("Information for /correlation-metrics retrieved from cache.")
        return CorrelationMetricsResponse(**data)
    try:
        period = f"{params.period_months}mo"
        prices_dict = get_close_prices_for_symbol(params.symbol, period, params.interval)
        benchmark_prices_dict = get_close_prices_for_symbol(params.benchmark, period, params.interval)
        if not prices_dict or not benchmark_prices_dict or len(prices_dict) != len(benchmark_prices_dict):
            raise HTTPException(status_code=404, detail="Not enough or mismatched price data for correlation/beta calculation.")

        prices = np.array([p["price"] for p in prices_dict])
        benchmark_prices = np.array([p["price"] for p in benchmark_prices_dict])
        returns = np.diff(prices) / prices[:-1]
        benchmark_returns = np.diff(benchmark_prices) / benchmark_prices[:-1]
        if len(returns) != len(benchmark_returns):
            min_len = min(len(returns), len(benchmark_returns))
            returns = returns[-min_len:]
            benchmark_returns = benchmark_returns[-min_len:]

        correlation = float(np.corrcoef(returns, benchmark_returns)[0, 1])
        beta = float(np.cov(returns, benchmark_returns)[0, 1] / np.var(benchmark_returns))

        response = CorrelationMetricsResponse(
            correlation=correlation,
            beta=beta
        )
        set_cache(cache_key, response.model_dump())
        return response
    except Exception as e:
        logger.exception(f"Error in correlation/beta metrics calculation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error in correlation/beta metrics calculation.")
