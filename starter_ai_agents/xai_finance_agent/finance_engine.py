import yfinance as yf
from typing import Dict, Any, Optional
from utils import setup_logger

logger = setup_logger(__name__)

class FinanceEngine:
    """
    Wrapper for YFinance to fetch stock and market data.
    """
    
    @staticmethod
    def get_stock_info(ticker: str) -> Dict[str, Any]:
        """Fetch basic stock info and current stats."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            return {
                "name": info.get("longName", ticker),
                "price": info.get("currentPrice"),
                "change_pct": info.get("regularMarketChangePercent"),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "summary": info.get("longBusinessSummary", "")
            }
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {e}")
            return {}

    @staticmethod
    def get_price_history(ticker: str, period: str = "1mo"):
        """Fetch price history for charting."""
        try:
            stock = yf.Ticker(ticker)
            return stock.history(period=period)
        except Exception as e:
            logger.error(f"Error fetching history for {ticker}: {e}")
            return None
