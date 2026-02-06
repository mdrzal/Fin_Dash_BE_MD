from fastapi import Depends, HTTPException
from app.models.schemas import PricesQueryParams, PricesResponse, PricePoint
from app.helpers.guards import validate_symbol, validate_interval
from app.services.financial_data import get_close_prices_for_symbol
from app.services.cache import get_cache, set_cache
from app.services.logging_service import LoggingService

logger = LoggingService.get_logger(__name__)

def prices_controller(params: PricesQueryParams = Depends()):
    validate_symbol(params.symbol)
    validate_interval(params.interval)
    cache_key = f"prices:{params.symbol}:{params.period_months}:{params.interval}"
    data = get_cache(cache_key)
    if data:
        logger.info("Information for /prices retrieved from cache.")
        return PricesResponse(prices=[PricePoint(**pt) for pt in data])
    try:
        period = f"{params.period_months}mo"
        price_points = get_close_prices_for_symbol(params.symbol, period, params.interval)
        prices = [PricePoint(price=pt["price"], date=pt["date"]) for pt in price_points]
        set_cache(cache_key, [pt.model_dump() for pt in prices])
        return PricesResponse(prices=prices)
    except Exception as e:
        logger.exception(f"Error in prices endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error in prices endpoint.")
