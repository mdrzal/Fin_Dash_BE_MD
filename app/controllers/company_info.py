from fastapi import HTTPException
from app.models.schemas import CompanyInfoQueryParams, CompanyInfoResponse
from app.helpers.guards import validate_symbol
from app.services.logging_service import LoggingService
import yfinance as yf

def company_info_controller(params: CompanyInfoQueryParams):
    logger = LoggingService.get_logger("company_info_controller")
    validate_symbol(params.symbol)
    try:
        ticker = yf.Ticker(params.symbol)
        info = ticker.info
        if not info:
            raise HTTPException(status_code=404, detail="No company info found for symbol.")
        response = CompanyInfoResponse(
            symbol=info.get("symbol", params.symbol),
            name=info.get("shortName") or info.get("longName") or info.get("symbol", params.symbol),
            sector=info.get("sector"),
            industry=info.get("industry"),
            website=info.get("website"),
            description=info.get("longBusinessSummary"),
            market_cap=info.get("marketCap")
        )
        return response
    except Exception as e:
        logger.exception(f"Error fetching company info: {e}")
        raise HTTPException(status_code=500, detail="Internal server error fetching company info.")
