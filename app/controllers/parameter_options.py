from app.models.schemas import IntervalEnum, MAWindowEnum, MAX_PERIOD_MONTHS, MIN_PERIOD_MONTHS
from app.services.cache import get_cache, set_cache

def parameter_options_controller():
    cache_key = "valid_parameter_options"
    data = get_cache(cache_key)
    if data:
        return data
    result = {
        "intervals": [e.value for e in IntervalEnum],
        "period_months": {"min": MIN_PERIOD_MONTHS, "max": MAX_PERIOD_MONTHS},
        "ma_windows": [e.value for e in MAWindowEnum],
    }
    set_cache(cache_key, result, ttl=3600)
    return result
