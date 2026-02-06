from fastapi import HTTPException
from app.models.schemas import (
    MovingAverageQueryParams, MovingAverageResponse
)
from app.helpers.guards import validate_symbol, validate_interval
from app.services.financial_data import get_close_prices_for_symbol
from app.services.analysis import calculate_moving_average
from app.services.logging_service import LoggingService
from app.services.cache import get_cache, set_cache


def moving_average_controller(params: MovingAverageQueryParams):
    logger = LoggingService.get_logger("moving_average_controller")
    validate_symbol(params.symbol)
    validate_interval(params.interval)
    cache_key = f"movingavg:{params.symbol}:{params.period_months}:{params.interval}:{params.window}"
    data = get_cache(cache_key)
    if data:
        logger.info("Information for /moving-average retrieved from cache.")
        return MovingAverageResponse(**data)
    try:
        period = f"{params.period_months}mo"
        price_points = get_close_prices_for_symbol(params.symbol, period, params.interval)
        price_values = [pt["price"] for pt in price_points]
        price_dates = [pt["date"] for pt in price_points]
        ma = calculate_moving_average(price_values, params.window)
        points = None
        if ma is not None:
            # Align moving average values with the last N dates
            relevant_dates = price_dates[-len(ma):] if len(price_dates) >= len(ma) else []
            points = [
                {"price": float(p), "date": d}
                for p, d in zip(ma, relevant_dates)
            ]
        response = MovingAverageResponse(moving_average=points)
        set_cache(cache_key, response.model_dump())
        return response
    except Exception as e:
        logger.exception(f"Error in moving average calculation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error in moving average calculation.")
