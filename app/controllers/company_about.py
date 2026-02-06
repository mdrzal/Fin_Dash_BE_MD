
import yfinance as yf
from fastapi import HTTPException
from ..models.schemas import CompanyInfoResponse, CompanyInfoQueryParams

def get_company_about(params: CompanyInfoQueryParams) -> CompanyInfoResponse:
    try:
        ticker_obj = yf.Ticker(params.symbol)
        info = ticker_obj.info
        if not info:
            raise ValueError('No company info found')
        return CompanyInfoResponse(
            symbol=info.get('symbol', params.symbol),
            name=info.get('shortName') or info.get('longName') or info.get('symbol', params.symbol),
            sector=info.get('sector'),
            industry=info.get('industry'),
            website=info.get('website'),
            description=info.get('longBusinessSummary'),
            market_cap=info.get('marketCap')
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Company info not found: {e}")
