import valutatrade_hub.core.utils as utils
import valutatrade_hub.core.models as models
import valutatrade_hub.decorators as decorators
import valutatrade_hub.core.currencies as currencies
import valutatrade_hub.core.exceptions as exceptions
import valutatrade_hub.infra.settings as settings
import valutatrade_hub.parser_service.config as config
import valutatrade_hub.parser_service.updater as updater
import valutatrade_hub.parser_service.api_clients as api_clients
import valutatrade_hub.parser_service.storage as storage
import random
import string
import datetime


def show_help():
    print(
        "Вызов команд:\n"
        "<command> <--argument1> <input> <--argument2> <input> ...\n"
        "\n"
        "Поддерживаемые коды валют: USD, EUR, GBP, RUB, BTC, ETH, SOL.\n"
        "\n"
        "Список команд:\n"
        "\n"
        "- register <--argument> <input> - регистрация в системе.\n"
        "Обязательные аргументы:\n"
        "--username <name> - имя пользователя. Не может быть пустым.\n"
        "--password <pass> - пароль. Должен содержать минимум 4 символа.\n"
        "\n"
        "- login <--argument> <input> - авторизация в системе.\n"
        "Обязательные аргументы:\n"
        "--username <name> - имя пользователя.\n"
        "--password <pass> - пароль.\n"
        "\n"
        "- show-portfolio <--argument> <input> - информация о ваших кошельках. Требует авторизации.\n"
        "Необязательные аргументы:\n"
        "--base <currency> - код валюты (например: USD), по которой учитывать общий баланс кошельков.\n"
        "\n"
        "- buy <--argument> <input> - купить валюту. Требует авторизации.\n"
        "Обязательные аргументы:\n"
        "--currency <currency> - код валюты (например: USD), которую хотите купить.\n"
        "--amount <currency> - объем покупки в штуках (например: 123.45). Неотрицательное число.\n"
        "\n"
        "- sell <--argument> <input> - продать валюту. Требует авторизации.\n"
        "Обязательные аргументы:\n"
        "--currency <currency> - код валюты (например: USD), которую хотите продать.\n"
        "--amount <currency> - объем продажи в штуках (например: 123.45). Неотрицательное число, нужно иметь необходимые средства в кошельке.\n"
        "\n"
        "- get-rate <--argument> <input> - получить курс одной валюты к другой.\n"
        "Обязательные аргументы:\n"
        "--from <currency> - код исходный валюты (например: EUR).\n"
        "--to <currency> - код целевой валюты (например: USD).\n"
        "\n"
        "- show-rates <--argument> <input> - получить курсы валют по фильтру.\n"
        "Необязательные аргументы:\n"
        "--currency <currency> - код исходной валюты (например: EUR).\n"
        "--base <currency> - код базовой валюты (например: USD).\n"
        "--top <value> - число (например: 5) верхних строк, которые хотите вывести на экран.\n"
        "\n"
        "- update-rates <--argument> <input> - обновить обменные курсы валют.\n"
        "Необязательные аргументы:\n"
        "--source <api> - один из сервисов API (coingecko или exchangerate). Если не указывать, будут задействованы оба сервиса.\n"
        "\n"
        "- exit - выход."
    )

def generate_salt(length):
    '''Возвращает строку длины length случайных символов'''
    salt = ''
    for i in range(length):
        salt += random.choice(string.printable)
    return str(salt)

@decorators.log_action(verbose=True)
def register_user(name=None, password=None):
    params = settings.SettingsLoader()
    if not name:
        raise ValueError("Имя пользователя не задано.")
    if not password:
        raise ValueError("Пароль не задан.")
    if len(password) < 4:
        raise ValueError("Пароль слишком короткий.")
    users_data = utils.load_json(params.USERS_PATH)
    for i in range(len(users_data)):
        if users_data[i]["username"] == name:
            raise ValueError("Такое имя уже существует.")
    user_id, i = 0, 0
    for i in range(len(users_data)):
        if user_id < int(users_data[i]["user_id"]):
            user_id = int(users_data[i]["user_id"])
    user_id += 1
    salt = generate_salt(length=params.SALT_LENGTH)
    current_time = datetime.datetime.now()
    new_user = models.User(user_id, name, password, salt, current_time)
    models.save_into_json(new_user)
    new_portfolio = models.Portfolio(user_id, dict())
    models.save_into_json(new_portfolio)
    logging_data = {
        "operation": "REGISTER",
        "user": name,
        "currency": '',
        "was_amount": '',
        "amount": '',
        "rate": '',
        "base": ''
    }
    return new_user, logging_data

@decorators.log_action(verbose=True)
def login_user(name=None, password=None):
    params = settings.SettingsLoader()
    if not name:
        raise ValueError("Имя пользователя не задано.")
    if not password:
        raise ValueError("Пароль не задан.")
    users_data = utils.load_json(params.USERS_PATH)
    for i in range(len(users_data)):
        if users_data[i]["username"] == name:
            existing_user = models.User(
                user_id = int(users_data[i]["user_id"]),
                username = users_data[i]["username"],
                hashed_password = users_data[i]["hashed_password"],
                salt = users_data[i]["salt"],
                registration_date = datetime.datetime.strptime(users_data[i]["registration_date"], "%Y-%m-%d %H:%M:%S")
            )
            existing_user.hashed_password = users_data[i]["hashed_password"]
            if not existing_user.verify_password(password):
                raise ValueError("Пароль неверный.")
            else:
                print(f"Вход в аккаунт '{name}'.")
                logging_data = {
                    "operation": "LOGIN",
                    "user": name,
                    "currency": '',
                    "was_amount": '',
                    "amount": '',
                    "rate": '',
                    "base": ''
                }
                return existing_user, logging_data
    raise ValueError("Пользователь не найден.")

def show_portfolio(base_currency, existing_user):
    params = settings.SettingsLoader()
    current_id = existing_user.user_id
    portfolios_data = utils.load_json(params.PORTFOLIOS_PATH)
    current_wallets = {}
    for i in range(len(portfolios_data)):
        if portfolios_data[i]["user_id"] == current_id:
            for key in portfolios_data[i]["wallets"]:
                key_currency_code = portfolios_data[i]["wallets"][key]["currency_code"]
                key_balance = portfolios_data[i]["wallets"][key]["balance"]
                current_wallets[key] = models.Wallet(currency_code=
                                                        key_currency_code,
                                                     balance=
                                                        key_balance)
            break
    if len(current_wallets) == 0:
        print("Кошельков нет.")
        return
    existing_portfolio = models.Portfolio(user_id=
                                            current_id,
                                          wallets=
                                            current_wallets)
    print(f"Портфель пользователя '{existing_user.username}' (база: {base_currency}):")
    crypto_service = api_clients.CoinGeckoClient()
    fiat_service = api_clients.ExchangeRateApiClient()
    storage_service = storage.StorageUpdater()
    updater_service = updater.RatesUpdater(crypto_service, fiat_service, storage_service)
    updater_service.run_update()
    existing_portfolio.get_total_value(base_currency)

@decorators.log_action(verbose=True)
def buy_by_user(currency, amount, existing_user):
    params = settings.SettingsLoader()
    cfg = config.ParserConfig()
    currency = currencies.get_currency(currency)
    if not amount:
        raise ValueError("Значение не задано.")
    amount = utils.parse_values(amount, 'float')[0]
    current_id = existing_user.user_id
    portfolios_data = utils.load_json(params.PORTFOLIOS_PATH)
    current_wallets = {}
    for i in range(len(portfolios_data)):
        if portfolios_data[i]["user_id"] == current_id:
            for key in portfolios_data[i]["wallets"]:
                key_currency_code = portfolios_data[i]["wallets"][key]["currency_code"]
                key_balance = portfolios_data[i]["wallets"][key]["balance"]
                current_wallets[key] = models.Wallet(currency_code=
                                                        key_currency_code,
                                                     balance=
                                                        key_balance)
            break
    existing_portfolio = models.Portfolio(user_id=
                                            current_id,
                                          wallets=
                                            current_wallets)
    if currency.code not in existing_portfolio.wallets.keys():
        existing_portfolio.add_currency(currency.code)
    balance_before = existing_portfolio.get_wallet(currency.code).balance
    existing_portfolio.get_wallet(currency.code).deposit(amount)
    base_currency = cfg.BASE_CURRENCY
    converse_way = currency.code + '_' + base_currency
    crypto_service = api_clients.CoinGeckoClient()
    fiat_service = api_clients.ExchangeRateApiClient()
    storage_service = storage.StorageUpdater()
    updater_service = updater.RatesUpdater(crypto_service, fiat_service, storage_service)
    updater_service.run_update()
    rates_json = utils.load_json(cfg.RATES_FILE_PATH)
    if not rates_json:
        raise ValueError("Кэш валют пуст. Воспользуйтесь командой 'update-rates'.")
    if converse_way not in rates_json["pairs"].keys():
        raise ValueError(f"Курс {converse_way} не найден.")
    multiplier = float(rates_json["pairs"][converse_way]["rate"])
    print(f"Покупка выполнена: {amount} {currency.code} по курсу {multiplier} {converse_way}\n"
          f"Изменения в портфеле:\n"
          f"- {currency.code}: было {balance_before} → стало {balance_before + amount}\n"
          f"Оценочная стоимость покупки: {amount * multiplier} {base_currency}")
    models.save_into_json(existing_portfolio)
    logging_data = {
        "operation": "BUY",
        "user": existing_user.username,
        "currency": currency.code,
        "was_amount": balance_before,
        "amount": amount,
        "rate": multiplier,
        "base": base_currency
    }
    return existing_user, logging_data

@decorators.log_action(verbose=True)
def sell_by_user(currency, amount, existing_user):
    params = settings.SettingsLoader()
    cfg = config.ParserConfig()
    currency = currencies.get_currency(currency)
    if not amount:
        raise ValueError("Значение не задано.")
    amount = utils.parse_values(amount, 'float')[0]
    current_id = existing_user.user_id
    portfolios_data = utils.load_json(params.PORTFOLIOS_PATH)
    current_wallets = {}
    for i in range(len(portfolios_data)):
        if portfolios_data[i]["user_id"] == current_id:
            for key in portfolios_data[i]["wallets"]:
                key_currency_code = portfolios_data[i]["wallets"][key]["currency_code"]
                key_balance = portfolios_data[i]["wallets"][key]["balance"]
                current_wallets[key] = models.Wallet(currency_code=
                                                        key_currency_code,
                                                     balance=
                                                        key_balance)
            break
    existing_portfolio = models.Portfolio(user_id=
                                            current_id,
                                          wallets=
                                            current_wallets)
    if currency.code not in existing_portfolio.wallets.keys():
        raise ValueError(f"Кошелек с '{currency.code}' не существует.")
    balance_before = existing_portfolio.get_wallet(currency.code).balance
    existing_portfolio.get_wallet(currency.code).withdraw(amount)
    base_currency = cfg.BASE_CURRENCY
    converse_way = currency.code + '_' + base_currency
    crypto_service = api_clients.CoinGeckoClient()
    fiat_service = api_clients.ExchangeRateApiClient()
    storage_service = storage.StorageUpdater()
    updater_service = updater.RatesUpdater(crypto_service, fiat_service, storage_service)
    updater_service.run_update()
    rates_json = utils.load_json(cfg.RATES_FILE_PATH)
    if not rates_json:
        raise ValueError("Кэш валют пуст. Воспользуйтесь командой 'update-rates'.")
    if converse_way not in rates_json["pairs"].keys():
        raise ValueError(f"Курс {converse_way} не найден.")
    multiplier = float(rates_json["pairs"][converse_way]["rate"])
    print(f"Продажа выполнена: {amount} {currency.code} по курсу {multiplier} {converse_way}\n"
          f"Изменения в портфеле:\n"
          f"- {currency.code}: было {balance_before} → стало {balance_before - amount}\n"
          f"Оценочная выручка: {amount * multiplier} {base_currency}")
    models.save_into_json(existing_portfolio)
    logging_data = {
        "operation": "SELL",
        "user": existing_user.username,
        "currency": currency.code,
        "was_amount": balance_before,
        "amount": amount,
        "rate": multiplier,
        "base": base_currency
    }
    return existing_user, logging_data

def get_rate_user(base_currency, pref_currency):
    cfg = config.ParserConfig()
    params = settings.SettingsLoader()
    base_currency = currencies.get_currency(base_currency)
    pref_currency = currencies.get_currency(pref_currency)
    converse_way_to = base_currency.code + '_' + pref_currency.code
    converse_way_from = pref_currency.code + '_' + base_currency.code
    rates_json = utils.load_json(cfg.RATES_FILE_PATH)
    if not rates_json:
        raise ValueError("Кэш валют пуст. Воспользуйтесь командой 'update-rates'.")
    if converse_way_to not in rates_json["pairs"].keys():
        raise ValueError(f"Курс {converse_way_to} не найден.")
    if converse_way_from not in rates_json["pairs"].keys():
        raise ValueError(f"Курс {converse_way_from} не найден.")
    multiplier_to = float(rates_json["pairs"][converse_way_to]["rate"])
    date_stamp_to = rates_json["pairs"][converse_way_to]["updated_at"]
    multiplier_from = float(rates_json["pairs"][converse_way_from]["rate"])
    print(f"Курс {base_currency.code}→{pref_currency.code}: {multiplier_to} (обновлено: {date_stamp_to})\n"
          f"Обратный курс {pref_currency.code}→{base_currency.code}: {multiplier_from}")
    last_update = datetime.datetime.strptime(date_stamp_to, "%Y-%m-%d %H:%M:%S")
    now_time = datetime.datetime.now()
    time_difference = now_time - last_update
    if time_difference > datetime.timedelta(seconds=int(params.RATES_TTL_SECONDS)):
        print(f"Данные устарели на {time_difference}. "
              f"Рекомендуется обновить курсы валют с помощью 'update-rates'.")

def show_rates_user(from_currency, top, to_currency):
    cfg = config.ParserConfig()
    params = settings.SettingsLoader()
    rates_json = utils.load_json(cfg.RATES_FILE_PATH)
    if not rates_json:
        raise ValueError("Кэш валют пуст. Воспользуйтесь командой 'update-rates'.")
    requested_rates = {}
    for key, value in rates_json["pairs"].items():
        key_from = str(key).split('_')[0]
        key_to = str(key).split('_')[1]
        if from_currency:
            if to_currency:
                if from_currency == key_from and to_currency == key_to:
                    requested_rates[key] = float(value["rate"])
            else:
                if from_currency == key_from:
                    requested_rates[key] = float(value["rate"])
        else:
            if to_currency:
                if to_currency == key_to:
                    requested_rates[key] = float(value["rate"])
            else:
                requested_rates[key] = float(value["rate"])
    if len(requested_rates) == 0:
        print("Не найдено курсов по такому фильтру.")
    else:
        print(f"Курсы валют из кэша (обновлено в {rates_json["last_refresh"]})")
        sorted_rates = {entry[0]: entry[1] for entry in sorted(requested_rates.items(), key=lambda arr:arr[1], reverse=True)}
        if not top:
            for key, value in sorted_rates.items():
                print(f"- {str(key)}: {value}")
        else:
            top = utils.parse_values(top, "int")[0]
            for key, value in sorted_rates.items():
                if top <= 0:
                    break
                print(f"- {str(key)}: {value}")
                top -= 1
        last_update = datetime.datetime.strptime(rates_json["last_refresh"], "%Y-%m-%d %H:%M:%S")
        now_time = datetime.datetime.now()
        time_difference = now_time - last_update
        if time_difference > datetime.timedelta(seconds=int(params.RATES_TTL_SECONDS)):
            print(f"Данные устарели на {time_difference}. "
                f"Рекомендуется обновить курсы валют с помощью 'update-rates'.")
