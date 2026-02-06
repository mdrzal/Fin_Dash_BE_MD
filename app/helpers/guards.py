from http.client import HTTPException
from pathlib import Path
import sqlite3
from app.models.schemas import IntervalEnum, MAWindowEnum, MAX_PERIOD_MONTHS, MIN_PERIOD_MONTHS

def validate_symbol(symbol: str):
    allowed = get_allowed_tickers()
    if symbol not in allowed:
        raise HTTPException(status_code=422, detail=f"Symbol '{symbol}' is not a valid/allowed ticker.")
    return symbol

def validate_period_months(period_months: int):
    if not (MIN_PERIOD_MONTHS <= period_months <= MAX_PERIOD_MONTHS):
        raise HTTPException(status_code=422, detail=f"period_months must be between {MIN_PERIOD_MONTHS} and {MAX_PERIOD_MONTHS}.")
    return period_months

def validate_ma_window(window: int):
    if window not in [e.value for e in MAWindowEnum]:
        raise HTTPException(status_code=422, detail=f"window must be one of {[e.value for e in MAWindowEnum]}.")
    return window

def validate_interval(interval: str):
    if interval not in [e.value for e in IntervalEnum]:
        raise HTTPException(status_code=422, detail=f"interval must be one of {[e.value for e in IntervalEnum]}.")
    return interval

def get_allowed_tickers():
    db_file = Path(__file__).parent.parent / 'database.db'
    conn = sqlite3.connect(str(db_file))
    c = conn.cursor()
    c.execute('SELECT symbol FROM stock_symbols')
    rows = c.fetchall()
    conn.close()
    return set(row[0] for row in rows)