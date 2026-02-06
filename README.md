

# Financial Analysis Backend

A modular, controller-based FastAPI backend for financial data analysis, supporting Yahoo Finance data fetching.


## Installation

### Local (without Docker)
1. Install all dependencies:
  ```
  pip install -r requirements.txt
  ```
2. Run the API server:
  ```
  uvicorn app.main:app --reload
  ```

### With Docker

1. Make sure that the docker is running

2. Build the Docker image:
  ```
  docker build -t financial-analysis-backend .
  ```
2. Run the container:
  ```
  docker run -p 8000:8000 financial-analysis-backend
  ```
The system will be available at http://127.0.0.1:8000/

## API Endpoints & Analysis Explanations

### Prices
- **GET /prices**
  - Query: `symbol` (str), `period_months` (int), `interval` (str)
  - Returns historical adjusted close prices as date/price pairs (adjusted for splits/dividends).
  - **Use:** For plotting price charts, comparing with moving averages, or as input to other analyses.

### Sentiment Analysis
- **GET /sentiment**
  - Query: `symbol` (str)
  - Returns sentiment score and recent news for the symbol.
  - **Use:** Gauge market mood. High positive sentiment may indicate bullishness; negative sentiment may warn of risk.

### Core Metrics
- **GET /core-metrics**
  - Query: `symbol`, `period_months`, `interval`, `rsi_period`, `ma_window`
  - Returns: Return, volatility, RSI, 1M/3M returns, P/E ratio.
  - **Explanations:**
    - **Return:** Total return over the period. Positive = gain, negative = loss.
    - **Volatility:** Standard deviation of returns. Higher = riskier.
    - **RSI:** Relative Strength Index (0-100). >70 = overbought, <30 = oversold.
    - **P/E Ratio:** Price/Earnings. High (>30) may mean overvalued; low (<10) may mean undervalued, but context matters.
    - **1M/3M Returns:** Returns over 1 and 3 months for short-term trend.

### Moving Average
- **GET /moving-average**
  - Query: `symbol`, `period_months`, `interval`, `window`
  - Returns: Moving average values as date/price pairs.
  - **Use:** Identify trends and support/resistance. Price above MA = uptrend; below = downtrend.

### Trend Metrics
- **GET /trend-metrics**
  - Query: `symbol`, `period_months`, `interval`
  - Returns: 20-day momentum, SMA gap, trend label.
  - **Explanations:**
    - **Momentum:** Price change over 20 days. Positive = upward momentum.
    - **SMA Gap:** Difference between price and 20-day SMA. Large positive gap = strong uptrend.
    - **Trend Label:** Simple uptrend/downtrend classification.

### Correlation Metrics
- **GET /correlation-metrics**
  - Query: `symbol`, `benchmark`, `period_months`, `interval`
  - Returns: Correlation and beta with respect to a benchmark (default: S&P 500).
  - **Explanations:**
    - **Correlation:** 1 = moves with benchmark, 0 = uncorrelated, -1 = moves opposite.
    - **Beta:** Sensitivity to benchmark. >1 = more volatile than market, <1 = less volatile.


### Drawdown Metrics
- **GET /drawdown-metrics**
  - Query: `symbol`, `period_months`, `interval`
  - Returns: Max drawdown percentage, recovery days.
  - **Explanations:**
    - **Max Drawdown:** Largest peak-to-trough loss. High drawdown = high risk.
    - **Recovery Days:** Days to recover from max drawdown. Shorter = more resilient.

### Company About
- **GET /company-about**
  - Query: `symbol` (str)
  - Returns: Company information including symbol, name, sector, industry, website, description, and market cap.
  - **Use:** Retrieve basic company profile and business summary for a given stock symbol.

### Available Tickers
- **GET /available-tickers**
  - Returns: List of all available stock tickers in the database.
  - **Use:** For populating dropdowns or validating user input.

### Recommendations
- **GET /recommendations**
  - Query: `symbol` (str)
  - Returns: Analyst recommendations for the given symbol.
  - **Use:** See consensus analyst opinion (buy/hold/sell).

### Valid Parameter Options
- **GET /valid-parameter-options**
  - Returns: All valid enum options and parameter constraints for the API.
  - **Use:** For frontend dropdowns, validation, and dynamic forms. Returns:
    - `intervals`: Allowed values for interval (e.g., '1d', '1h', '1wk')
    - `period_months`: Min/max allowed for period_months
    - `ma_windows`: Allowed window sizes for moving average

## Parameter Validation & Enums

All endpoints strictly validate input parameters using enums and constraints:
- **Intervals:** 
- **Moving Average Windows:** 
- **Period Months:** 

## Caching Approach

This project uses in-memory cache for all endpoints. The cache is implemented in Python and does not require any external services (like Redis). By default, cached items expire after 10 minutes (600 seconds).

**Why in-memory cache?**
- Simplicity: No need to install or run redis.
- Portability: The backend works out-of-the-box for local development and personal use which was intended for this software.

**Intended Use:**
This backend is designed as a local analysis tool or for personal dashboards, not as a high-availability, multi-user production API.

### Running with the Backend
To pair the backend with the frontend:

 ---placeholder