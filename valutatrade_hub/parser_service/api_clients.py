import requests
import datetime
import valutatrade_hub.core.exceptions as exceptions
import valutatrade_hub.parser_service.config as config


class BaseApiClient:
    def fetch_rates():
        return None

class CoinGeckoClient(BaseApiClient):
    def fetch_rates():
        '''
        Парсит данные: {
            "bitcoin":  { "usd": 59337.21 },
            "ethereum": { "usd": 3720.00 },
            "solana":   { "usd": 145.12 }
        }
        Вывод: {
            "BTC_USD: { "rate": 59337.21, "updated_at": "2025-10-10T12:00:00Z", "source": "CoinGecko" },
            ...
        }
        '''
        cfg = config.ParserConfig()
        line_ids = ""
        for currency in cfg.CRYPTO_CURRENCIES:
            currency_id = cfg.CRYPTO_ID_MAP[currency]
            line_ids += currency_id + ','
        line_ids = line_ids[:-1]
        # https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd
        url = cfg.COINGECKO_URL + "?ids=" + line_ids + "&vs_currencies=" + cfg.BASE_CURRENCY.lower()
        try:
            crypto_info = requests.get(url).json()
            update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result = {}
            for key in crypto_info.keys():
                for cur, val in cfg.CRYPTO_ID_MAP:
                    if str(key) == val:
                        parsed_cur = cur
                        break
                result[parsed_cur + "_" + cfg.BASE_CURRENCY] = {
                    "rate": crypto_info[key][cfg.BASE_CURRENCY.lower()],
                    "updated_at": update_time,
                    "source": "CoinGecko"
                }
            return result
        except requests.RequestException as e:
            raise exceptions.ApiRequestError("Ошибка обращения к 'api.coingeckoo.com'.")

class ExchangeRateApiClient(BaseApiClient):
    def fetch_rates():
        '''
        Парсит данные: {
            "result":"success",
            "documentation":"https://www.exchangerate-api.com/docs",
            "terms_of_use":"https://www.exchangerate-api.com/terms",
            "time_last_update_unix":1765065601,
            "time_last_update_utc":"Sun, 07 Dec 2025 00:00:01 +0000",
            "time_next_update_unix":1765152001,
            "time_next_update_utc":"Mon, 08 Dec 2025 00:00:01 +0000",
            "base_code":"USD",
            "conversion_rates":{
                "USD":1,
                "AED":3.6725,
                "AFN":66.2641,
                "ALL":82.8927,
                ...
            }
        }
        Вывод: {
            "EUR_USD: { "rate": 59337.21, "updated_at": "2025-10-10T12:00:00Z", "source": "ExchangeRate-API" },
            ...
        }
        '''
        cfg = config.ParserConfig()
        # https://v6.exchangerate-api.com/v6/1e0758931d900d0ccdbe6ed2/latest/USD
        url = cfg.EXCHANGERATE_API_URL + "/" + cfg.EXCHANGERATE_API_KEY + "/latest/" + cfg.BASE_CURRENCY
        try:
            fiat_info = requests.get(url).json()
            if fiat_info["result"] != "success":
                raise exceptions.ApiRequestError("Ошибка обращения к 'v6.exchangerate-api.com'.")
            update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result = {}
            for currency in cfg.FIAT_CURRENCIES:
                result[currency + "_" + cfg.BASE_CURRENCY] = {
                    "rate": fiat_info["conversion_rates"][currency],
                    "updated_at": update_time,
                    "source": "ExchangeRate-API"
                }
            return result
        except requests.RequestException as e:
            raise exceptions.ApiRequestError("Ошибка обращения к 'v6.exchangerate-api.com'.")
