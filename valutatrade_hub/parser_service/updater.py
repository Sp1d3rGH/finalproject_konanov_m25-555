import datetime
import valutatrade_hub.parser_service.config as config
import valutatrade_hub.parser_service.api_clients as api_clients
import valutatrade_hub.parser_service.storage as storage


class RatesUpdater:
    def __init__(self,
                 crypto_api: api_clients.CoinGeckoClient,
                 fiat_api: api_clients.ExchangeRateApiClient,
                 storage: storage.StorageUpdater):
        self.crypto_api = crypto_api
        self.fiat_api = fiat_api
        self.storage = storage

    def run_update(self):
        rates = {"pairs": {}}
        crypto_output = self.crypto_api.fetch_rates()
        fiat_output = self.fiat_api.fetch_rates()
        for key_rate in crypto_output:
            rates["pairs"][key_rate] = crypto_output[key_rate]
        for key_rate in fiat_output:
            rates["pairs"][key_rate] = fiat_output[key_rate]
        rates["last_refresh"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.storage.save_to_json(rates)
