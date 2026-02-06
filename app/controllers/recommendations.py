from fastapi import HTTPException
from app.models.schemas import RecommendationsQueryParams
from app.helpers.guards import validate_symbol
from app.services.financial_data import get_recomendations_for_symbol
from app.services.logging_service import LoggingService
from app.services.cache import get_cache, set_cache
import pandas as pd
import numpy as np

def convert_numpy_types(obj):
    if isinstance(obj, np.generic):
        return obj.item()
    return obj

def recommendations_controller(params: RecommendationsQueryParams):
    logger = LoggingService.get_logger("recommendations_controller")
    validate_symbol(params.symbol)
    cache_key = f"recommendations:{params.symbol}"
    data = get_cache(cache_key)
    if data:
        logger.info("Information for /recommendations retrieved from cache.")
        return data
    try:
        result = get_recomendations_for_symbol(params.symbol)
        if isinstance(result, pd.DataFrame):
            data = result.to_dict(orient="records")
            # Convert negative period values to positive (e.g., '-1m' to '1m')
            for row in data:
                if "period" in row and isinstance(row["period"], str) and row["period"].startswith("-"):
                    row["period"] = row["period"][1:]
            data = [{k: convert_numpy_types(v) for k, v in row.items()} for row in data]
            set_cache(cache_key, data)
            return data
        set_cache(cache_key, result)
        return result
    except Exception as e:
        logger.exception(f"Error in getting recommendations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error in sentiment analysis.")
