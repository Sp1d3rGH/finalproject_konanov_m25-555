from dataclasses import dataclass
import os


@dataclass
class ParserConfig:
    # EXCHANGERATE_API_KEY: str = os.getenv("EXCHANGERATE_API_KEY")
    EXCHANGERATE_API_KEY: str = "1e0758931d900d0ccdbe6ed2" # ПОТОМ ПОМЕНЯТЬ
    COINGECKO_URL: str = "https://api.coingecko.com/api/v3/simple/price"
    EXCHANGERATE_API_URL: str = "https://v6.exchangerate-api.com/v6"
    BASE_CURRENCY: str = "USD"
    FIAT_CURRENCIES: tuple = ("EUR", "GBP", "RUB")
    FIAT_ID_MAP: dict = {
        "EUR": "Euro",
        "GBP": "Sterling",
        "RUB": "Ruble"
    }
    CRYPTO_CURRENCIES: tuple = ("BTC", "ETH", "SOL")
    CRYPTO_ID_MAP: dict = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "SOL": "solana"
    }
    RATES_FILE_PATH: str = "data/rates.json"
    HISTORY_FILE_PATH: str = "data/exchange_rates.json"
    REQUEST_TIMEOUT: int = 10
