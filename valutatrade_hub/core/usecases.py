import valutatrade_hub.core.utils as utils
import valutatrade_hub.core.models as models
import random
import string
import datetime


USERS_PATH = "data/users.json"
PORTFOLIOS_PATH = "data/portfolios.json"
RATES_PATH = "data/rates.json"
EXCHANGE_RATES_PATH = "data/exchange_rates.json"
SALT_LENGTH = 8

def show_help():
    print("- зарегистрироваться (register);\n"
    "- войти в систему (login);\n"
    "- посмотреть свой портфель и балансы (show-portfolio);\n"
    "- купить валюту (buy);\n"
    "- продать валюту (sell);\n"
    "- получить курс валюты (get-rate).")

def generate_salt(length=4):
    salt = ''
    for i in range(length):
        salt += random.choice(string.printable)
    return str(salt)

def register_user(name=None, password=None):
    if not name:
        raise ValueError("Имя пользователя не задано.")
    if not password:
        raise ValueError("Пароль не задан.")
    if len(password) < 4:
        raise ValueError("Пароль слишком короткий.")
    users_data = utils.load_json(USERS_PATH)
    for i in range(len(users_data)):
        if users_data[i]["username"] == name:
            raise ValueError("Такое имя уже существует.")
    user_id = 0
    for i in range(len(users_data)):
        if user_id < users_data[i]["user_id"]:
            user_id = users_data[i]["user_id"]
    user_id = i + 1
    salt = generate_salt(length=SALT_LENGTH)
    current_time = datetime.datetime.now()
    new_user = models.User(user_id, name, password, salt, current_time)
    new_user.save_to_json()
    new_portfolio = models.Portfolio(user_id, dict())
    new_portfolio.save_to_json()
    # return new_user, new_portfolio

def login_user(name=None, password=None):
    if not name:
        raise ValueError("Имя пользователя не задано.")
    if not password:
        raise ValueError("Пароль не задан.")
    users_data = utils.load_json(USERS_PATH)
    for i in range(len(users_data)):
        if users_data[i]["username"] == name:
            existing_user = models.User(user_id=
                                            int(users_data[i]["user_id"]),
                                        username=
                                            users_data[i]["username"],
                                        hashed_password=
                                            users_data[i]["hashed_password"],
                                        salt=
                                            users_data[i]["salt"],
                                        registration_date=
                                            datetime.datetime(users_data[i]["registration_date"]))
            if not existing_user.verify_password(password):
                raise ValueError("Пароль неверный.")
            else:
                return existing_user
    raise ValueError("Пользователь не найден.")

def show_portfolio(base_currency, existing_user):
    current_id = existing_user.user_id
    portfolios_data = utils.load_json(PORTFOLIOS_PATH)
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
    existing_portfolio.get_total_value(base_currency)

def buy_by_user(currency, amount, existing_user):
    if not currency:
        raise ValueError("Валюта не задана.")
    if not amount:
        raise ValueError("Значение не задано.")
    amount = utils.parse_values(amount, 'float')[0]
    current_id = existing_user.user_id
    portfolios_data = utils.load_json(PORTFOLIOS_PATH)
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
    if currency not in existing_portfolio.wallets.keys():
        existing_portfolio.add_currency(currency)
    balance_before = existing_portfolio.get_wallet(currency).balance
    existing_portfolio.get_wallet(currency).deposit(amount)
    base_currency = 'USD'
    converse_way = currency + '_' + base_currency
    exchange_rates_json = utils.load_json(EXCHANGE_RATES_PATH)
    if converse_way not in exchange_rates_json.keys():
        raise ValueError(f"Курс {converse_way} не найден.")
    multiplier = float(exchange_rates_json[converse_way]["rate"])
    print(f"Покупка выполнена: {amount} {currency} по курсу {multiplier} {converse_way}\n"
          f"Изменения в портфеле:\n"
          f"- {currency}: было {balance_before} → стало {balance_before + amount}\n"
          f"Оценочная стоимость покупки: {amount * multiplier} {base_currency}")
    existing_portfolio.save_to_json()

def sell_by_user(currency, amount, existing_user):
    if not currency:
        raise ValueError("Валюта не задана.")
    if not amount:
        raise ValueError("Значение не задано.")
    amount = utils.parse_values(amount, 'float')[0]
    current_id = existing_user.user_id
    portfolios_data = utils.load_json(PORTFOLIOS_PATH)
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
    if currency not in existing_portfolio.wallets.keys():
        raise ValueError(f"Кошелек с '{currency}' не существует.")
    balance_before = existing_portfolio.get_wallet(currency).balance
    existing_portfolio.get_wallet(currency).withdraw(amount)
    base_currency = 'USD'
    converse_way = currency + '_' + base_currency
    exchange_rates_json = utils.load_json(EXCHANGE_RATES_PATH)
    if converse_way not in exchange_rates_json.keys():
        raise ValueError(f"Курс {converse_way} не найден.")
    multiplier = float(exchange_rates_json[converse_way]["rate"])
    print(f"Продажа выполнена: {amount} {currency} по курсу {multiplier} {converse_way}\n"
          f"Изменения в портфеле:\n"
          f"- {currency}: было {balance_before} → стало {balance_before - amount}\n"
          f"Оценочная выручка: {amount * multiplier} {base_currency}")
    existing_portfolio.save_to_json()

def get_rate_user(base_currency, pref_currency):
    if not base_currency:
        raise ValueError("Базовая валюта не задана.")
    if not pref_currency:
        raise ValueError("Целевая валюта не задана.")
    converse_way_to = base_currency + '_' + pref_currency
    converse_way_from = pref_currency + '_' + base_currency
    exchange_rates_json = utils.load_json(EXCHANGE_RATES_PATH)
    if converse_way_to not in exchange_rates_json.keys():
        raise ValueError(f"Курс {converse_way_to} не найден.")
    if converse_way_from not in exchange_rates_json.keys():
        raise ValueError(f"Курс {converse_way_from} не найден.")
    multiplier_to = float(exchange_rates_json[converse_way_to]["rate"])
    date_stamp_to = datetime.datetime(exchange_rates_json[converse_way_to]["rate"])
    multiplier_from = float(exchange_rates_json[converse_way_from]["rate"])
    # date_stamp_from = datetime.datetime(exchange_rates_json[converse_way_from]["rate"])
    print(f"Курс {base_currency}→{pref_currency}: {multiplier_to} (обновлено: {date_stamp_to})\n"
          f"Обратный курс {pref_currency}→{base_currency}: {multiplier_from}")
