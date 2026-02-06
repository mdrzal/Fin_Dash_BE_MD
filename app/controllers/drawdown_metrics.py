from fastapi import HTTPException
from app.models.schemas import (
    DrawdownMetricsQueryParams, DrawdownMetricsResponse
)
from app.helpers.guards import validate_symbol, validate_interval
from app.services.financial_data import get_close_prices_for_symbol
from app.services.logging_service import LoggingService
from app.services.cache import get_cache, set_cache
import numpy as np


def drawdown_metrics_controller(params: DrawdownMetricsQueryParams):
    logger = LoggingService.get_logger("drawdown_metrics_controller")
    validate_symbol(params.symbol)
    validate_interval(params.interval)
    cache_key = f"drawdown:{params.symbol}:{params.period_months}:{params.interval}"
    data = get_cache(cache_key)
    if data:
        logger.info("Information for /drawdown-metrics retrieved from cache.")
        return DrawdownMetricsResponse(**data)
    try:
        period = f"{params.period_months}mo"
        prices_dict = get_close_prices_for_symbol(params.symbol, period, params.interval)
        if not prices_dict or len(prices_dict) < 2:
            raise HTTPException(status_code=404, detail="Not enough price data for drawdown analysis.")

        prices = np.array([p["price"] for p in prices_dict])
        running_max = np.maximum.accumulate(prices)
        drawdowns = (prices - running_max) / running_max
        max_drawdown = float(drawdowns.min())
        max_drawdown_pct = abs(max_drawdown) * 100

        # Recovery days: days from max drawdown to recovery above previous peak
        drawdown_idx = np.argmin(drawdowns)
        peak_idx = np.argmax(prices[:drawdown_idx+1])
        recovery_idx = None
        for i in range(drawdown_idx, len(prices)):
            if prices[i] >= running_max[peak_idx]:
                recovery_idx = i
                break
        recovery_days = (recovery_idx - drawdown_idx) if recovery_idx is not None else None

        response = DrawdownMetricsResponse(
            max_drawdown_pct=float(max_drawdown_pct),
            recovery_days=int(recovery_days) if recovery_days is not None else None
        )
        set_cache(cache_key, response.model_dump())
        return response
    except Exception as e:
        logger.exception(f"Error in drawdown metrics calculation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error in drawdown metrics calculation.")
