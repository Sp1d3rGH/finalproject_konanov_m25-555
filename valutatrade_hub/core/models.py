import hashlib
import datetime
import valutatrade_hub.core.utils as utils
import valutatrade_hub.core.exceptions as exceptions
import valutatrade_hub.infra.settings as settings
import valutatrade_hub.parser_service.config as config


class User:
    def __init__(self, user_id=None, username=None, hashed_password=None, salt=None, registration_date=None):
        if (isinstance(user_id, int) and
            isinstance(username, str) and
            isinstance(hashed_password, str) and
            isinstance(salt, str) and
            isinstance(registration_date, datetime.datetime)):
            pass
        else:
            raise TypeError("Некорректный тип данных для класса User.")
        self._user_id = user_id
        self._username = username
        self._hashed_password = self.get_hash(hashed_password + salt)
        self._salt = salt
        self._registration_date = registration_date

    @property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, value):
        if not isinstance(value, str):
            raise TypeError(type(value))
        self._user_id = value

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, value):
        if not isinstance(value, str):
            raise TypeError(type(value))
        if value == '':
            raise ValueError("Имя не может быть пустым.")
        self._username = value

    @property
    def hashed_password(self):
        return self._hashed_password
    
    @hashed_password.setter
    def hashed_password(self, value):
        if not isinstance(value, str):
            raise TypeError(type(value))
        if len(value) < 4:
            raise ValueError("Пароль не должен быть короче 4 символов.")
        self._hashed_password = value

    @property
    def salt(self):
        return self._salt
    
    @salt.setter
    def salt(self, value):
        if not isinstance(value, str):
            raise TypeError(type(value))
        self._salt = value

    @property
    def registration_date(self):
        return self._registration_date
    
    @registration_date.setter
    def registration_date(self, value):
        if not isinstance(value, datetime.datetime):
            raise TypeError(type(value))
        self._registration_date = value

    def get_user_info(self):
        reg_date = self.registration_date
        print(f"Данные пользователя '{self.username}':\n"
              f"- ID в системе: {self.user_id}\n"
              f"- Дата регистрации: {reg_date.strftime("%Y-%m-%d %H:%M:%S")}")

    def change_password(self, new_password=None):
        self.hashed_password = self.get_hash(new_password + self.salt)

    def verify_password(self, password):
        pass_to_check = self.get_hash(password + self.salt)
        return self.hashed_password == pass_to_check

    @staticmethod
    def get_hash(string):
        if not isinstance(string, str):
            raise TypeError(type(string))
        sha256 = hashlib.sha256()
        sha256.update(string.encode("utf-8"))
        sha256_string = sha256.hexdigest()
        return sha256_string

class Wallet:
    def __init__(self, currency_code=None, balance=None):
        if (isinstance(currency_code, str) and
            isinstance(balance, float)):
            pass
        else:
            raise TypeError("Некорректный тип данных для класса Wallet.")
        self._currency_code = currency_code
        self._balance = balance

    @property
    def currency_code(self):
        return self._currency_code
    
    @currency_code.setter
    def currency_node(self, value):
        if not isinstance(value, str):
            raise TypeError(type(value))
        self._currency_code = value
    
    @property
    def balance(self):
        return self._balance
    
    @balance.setter
    def balance(self, value):
        if not isinstance(value, float):
            raise TypeError(type(value))
        if value < 0:
            raise ValueError("Отрицательное значение.")
        self._balance = value
    
    def deposit(self, amount):
        if not isinstance(amount, float):
            raise TypeError(type(amount))
        if amount < 0:
            raise ValueError("Отрицательное значение.")
        self.balance += amount

    def withdraw(self, amount):
        if not isinstance(amount, float):
            raise TypeError(type(amount))
        if self.balance < amount:
            raise exceptions.InsufficientFundsError(self.currency_code, self.balance, amount)
        if amount < 0:
            raise ValueError("Отрицательное значение.")
        self.balance -= amount
    
    def get_balance_info(self):
        print("Доступные средства:", self.balance, self.currency_code)

class Portfolio:
    def __init__(self, user_id=None, wallets=None):
        if (isinstance(user_id, int) and
            isinstance(wallets, dict)):
            pass
        else:
            raise TypeError("Некорректный тип данных для класса Portfolio.")
        self._user_id = user_id
        self._wallets = wallets

    @property
    def user_id(self):
        return self._user_id
    
    @property
    def wallets(self):
        return self._wallets
    
    @wallets.setter
    def wallets(self, dictionary):
        if not isinstance(dictionary, dict):
            raise TypeError(type(dictionary))
        for key in dictionary:
            if not isinstance(key, str):
                raise TypeError(type(key))
            if not isinstance(dictionary[key], Wallet):
                raise TypeError(type(dictionary[key]))
        self._wallets = dictionary

    def add_currency(self, currency_code):
        cfg = config.ParserConfig()
        if not isinstance(currency_code, str):
            raise TypeError(type(currency_code))
        if currency_code in self.wallets.keys():
            raise ValueError(f"Счет {currency_code} уже существует.")
        if (currency_code not in cfg.FIAT_CURRENCIES and
            currency_code not in cfg.CRYPTO_CURRENCIES):
            raise exceptions.CurrencyNotFoundError(currency_code)
        self.wallets[currency_code] = Wallet(currency_code, 0.0)

    def get_total_value(self, base_currency='USD'):
        if not isinstance(base_currency, str):
            raise TypeError(type(base_currency))
        total_value = 0.0
        for currency in self.wallets.keys():
            currency_balance = self.wallets[currency].balance
            result = self.converse_to_base(str(currency), base_currency, currency_balance)
            total_value += result
            print(f"- {str(currency)}: {currency_balance}  → {result} {base_currency}")
        print(f"---------------------------------\n"
              f"ИТОГО: {total_value} {base_currency}")
        return total_value
    
    def get_wallet(self, currency_code):
        if not isinstance(currency_code, str):
            raise TypeError(type(currency_code))
        if currency_code not in self.wallets.keys():
            raise ValueError(f"Счет {currency_code} не существует.")
        return self.wallets[currency_code]

    @staticmethod
    def converse_to_base(current_currency, base_currency, amount):
        cfg = config.ParserConfig()
        converse_way = current_currency + '_' + base_currency
        rates_json = utils.load_json(cfg.RATES_FILE_PATH)
        if not rates_json:
            raise ValueError("Кэш валют пуст. Воспользуйтесь командой 'update-rates'.")
        if converse_way not in rates_json["pairs"].keys():
            raise ValueError(f"Курс {converse_way} не найден.")
        multiplier = float(rates_json["pairs"][converse_way]["rate"])
        return amount * multiplier

def save_into_json(model_class):
    params = settings.SettingsLoader()
    if isinstance(model_class, User):
        json_path = params.USERS_PATH
        json_data = utils.load_json(json_path)
        save_location = -1
        for i in range(len(json_data)):
            if json_data[i]["user_id"] == model_class.user_id:
                save_location = i
                break
        if save_location < 0:
            json_data.append({
                "user_id": None,
                "username": None,
                "hashed_password": None,
                "salt": None,
                "registration_date": None
            })
        json_data[save_location]["user_id"] = model_class.user_id
        json_data[save_location]["username"] = model_class.username
        json_data[save_location]["hashed_password"] = model_class.hashed_password
        json_data[save_location]["salt"] = model_class.salt
        json_data[save_location]["registration_date"] = model_class.registration_date.strftime("%Y-%m-%d %H:%M:%S")
        utils.save_json(json_path, json_data)
    elif isinstance(model_class, Portfolio):
        json_path = params.PORTFOLIOS_PATH
        json_data = utils.load_json(json_path)
        save_location = -1
        for i in range(len(json_data)):
            if json_data[i]["user_id"] == model_class.user_id:
                save_location = i
                break
        if save_location < 0:
            json_data.append({
                "user_id": None,
                "wallets": {}
            })
        json_data[save_location]["user_id"] = model_class.user_id
        wallets_dictionary = {}
        for key in model_class.wallets.keys():
            wallets_dictionary[key] = {
                "currency_code": model_class.wallets[key].currency_code,
                "balance": model_class.wallets[key].balance
                }
        json_data[save_location]["wallets"] = wallets_dictionary
        utils.save_json(json_path, json_data)
    else:
        raise TypeError("Неподдерживаемый класс для сохранения в json.")
