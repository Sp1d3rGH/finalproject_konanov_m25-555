import datetime
import valutatrade_hub.parser_service.config as config
import valutatrade_hub.parser_service.api_clients as api_clients
import valutatrade_hub.parser_service.storage as storage
import valutatrade_hub.core.exceptions as exceptions


class RatesUpdater:
    def __init__(self,
                 crypto_api: api_clients.CoinGeckoClient,
                 fiat_api: api_clients.ExchangeRateApiClient,
                 storage: storage.StorageUpdater,
                 input_source):
        self.crypto_api = crypto_api
        self.fiat_api = fiat_api
        self.storage = storage
        self.input_source = input_source.lower()
        self.cfg = config.ParserConfig()

    def run_update(self):
        errors = False
        rates = {"pairs": {}}
        update_crypto = True
        update_fiat = True
        match self.input_source:
            case "coingecko":
                update_fiat = False
            case "exchangerate":
                update_crypto = False
            case '':
                pass
        print("INFO: Обновление курсов валют...")
        if update_crypto == True:
            try:
                print("INFO: Запрос с CoinGecko...", end='')
                crypto_output = {}
                crypto_output = self.crypto_api.fetch_rates()
                print(f"OK ({len(crypto_output)})")
            except exceptions.ApiRequestError as e:
                errors = True
                print(f"ERROR ({e})")
        elif update_fiat == True:
            try:
                print("INFO: Запрос с ExchangeRate-API...", end='')
                fiat_output = {}
                fiat_output = self.fiat_api.fetch_rates()
                print(f"OK ({len(fiat_output)})")
            except exceptions.ApiRequestError as e:
                errors = True
                print(f"ERROR ({e})")
        else:
            raise exceptions.ApiRequestError("Не выбраны сервисы для обращения.")
        for key_rate in crypto_output:
            rates["pairs"][key_rate] = crypto_output[key_rate]
        for key_rate in fiat_output:
            rates["pairs"][key_rate] = fiat_output[key_rate]
        rates["last_refresh"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"INFO: Запись {len(rates["pairs"])} курсов "
              f"в {self.cfg.RATES_FILE_PATH}...")
        self.storage.save_rates(rates)
        if not errors:
            print(f"Обновление успешно. "
                  f"Всего обновленных записей: {len(rates["pairs"])}. "
                  f"Последнее обновление: {rates["last_refresh"]}")
        else:
            print(f"Обновление выполнено с ошибками.")
        history_update = {}
        for key, value in rates["pairs"]:
            history_from_currency = str(key).split('_')[0]
            history_to_currency = str(key).split('_')[1]
            history_rate = value["rate"]
            history_timestamp = value["updated_at"]
            history_source = value["source"]
            history_id = str(key) + '_' + value["updated_at"]
            history_update[history_id] = {
                "id": history_id,
                "from_currency": history_from_currency,
                "to_currency": history_to_currency,
                "rate": history_rate,
                "timestamp": history_timestamp,
                "source": history_source,
                "meta": {
                    "raw_id": None
                }
            }
        self.storage.save_history(history_update)
