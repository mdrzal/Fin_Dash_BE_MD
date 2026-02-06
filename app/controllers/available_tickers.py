from fastapi import HTTPException
from app.services.logging_service import LoggingService
from app.models.schemas import AvailableTickersQueryParams, AvailableTickersResponse, AvailableTicker
from app.db import get_db_connection

logger = LoggingService.get_logger("available_tickers_controller")
MAX_TICKERS = 20

def available_tickers_controller(params: AvailableTickersQueryParams):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        if params.starts_with:
            starts_with = params.starts_with.upper()
            c.execute(
                "SELECT symbol, name FROM stock_symbols WHERE symbol LIKE ? ORDER BY symbol ASC LIMIT ?",
                (f"{starts_with}%", MAX_TICKERS)
            )
        else:
            c.execute(
                "SELECT symbol, name FROM stock_symbols ORDER BY symbol ASC LIMIT ?",
                (MAX_TICKERS,)
            )
        rows = c.fetchall()
        tickers = [AvailableTicker(symbol=row[0], name=row[1]) for row in rows]
        return AvailableTickersResponse(tickers=tickers)
    except Exception as e:
        logger.exception(f"Error fetching available tickers: {e}")
        raise HTTPException(status_code=500, detail="Internal server error fetching available tickers.")
