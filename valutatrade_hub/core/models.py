import hashlib
import datetime
import valutatrade_hub.core.utils as utils
import valutatrade_hub.core.exceptions as exceptions


USD_CONVERSION = 1.0
DATA_DIR = "data"
RATES_PATH = "data/rates.json"
EXCHANGE_RATES_PATH = "data/exchange_rates.json"
KNOWN_CURRENCIES = ["USD", "EUR", "BTC", "ETH"]

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
        self.user_id = user_id
        self.username = username
        self.hashed_password = self.get_hash(hashed_password + salt)
        self.salt = salt
        self.registration_date = registration_date

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

    @classmethod
    def get_user_info(self):
        print(f"Данные пользователя '{self._username}':\n"
              f"{self._registration_date}")

    @classmethod
    def change_password(self, new_password=None):
        self.hashed_password = self.get_hash(new_password + self.salt)

    @classmethod
    def verify_password(self, password):
        pass_to_check = self.get_hash(password + self.salt)
        return password == pass_to_check
    
    @classmethod
    def save_to_json(self, json_name="users.json"):
        json_path = DATA_DIR + '/' + json_name
        json_data = utils.load_json(json_path)
        save_location = -1
        for i in range(len(json_data)):
            if json_data[i]["user_id"] == self.user_id:
                save_location = i
                break
        if save_location < 0 and len(json_data) == 0:
            json_data.append({
                "user_id": None,
                "username": None,
                "hashed_password": None,
                "salt": None,
                "registration_date": None
            })
            save_location = 0
        json_data[save_location]["user_id"] = self.user_id
        json_data[save_location]["username"] = self.username
        json_data[save_location]["hashed_password"] = self.hashed_password
        json_data[save_location]["salt"] = self.salt
        json_data[save_location]["registration_date"] = self.registration_date
        utils.save_json(json_path, json_data)

    @staticmethod
    def get_hash(string):
        if not isinstance(string, str):
            raise TypeError(type(string))
        sha256 = hashlib.sha256()
        sha256.update(string)
        sha256_string = sha256.hexdigest()
        return sha256_string

class Wallet:
    def __init__(self, currency_code=None, balance=None):
        if (isinstance(currency_code, str) and
            isinstance(balance, float)):
            pass
        else:
            raise TypeError("Некорректный тип данных для класса Wallet.")
        self.currency_code = currency_code
        self.balance = balance

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
            raise TypeError("Отрицательное значение.")
        self._balance = value
    
    @classmethod
    def deposit(self, amount):
        if not isinstance(amount, float):
            raise TypeError(type(amount))
        if amount < 0:
            raise TypeError("Отрицательное значение.")
        self.balance += amount

    @classmethod
    def withdraw(self, amount):
        if not isinstance(amount, float):
            raise TypeError(type(amount))
        if self.balance < amount:
            raise exceptions.InsufficientFundsError(self.currency_code, self.balance, amount)
        if amount < 0:
            raise TypeError("Отрицательное значение.")
        self.balance -= amount
    
    @classmethod
    def get_balance_info(self):
        print("Доступные средства:", self.balance, self.currency_code)

class Portfolio:
    def __init__(self, user_id=None, wallets=None):
        if (isinstance(user_id, str) and
            isinstance(wallets, dict)):
            pass
        else:
            raise TypeError("Некорректный тип данных для класса Portfolio.")
        self._user_id = user_id
        self.wallets = wallets

    @property
    def user_id(self): # ? class 'User' ?
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

    @classmethod
    def add_currency(self, currency_code):
        if not isinstance(currency_code, str):
            raise TypeError(type(currency_code))
        if currency_code in self.wallets.keys():
            raise ValueError(f"Счет {currency_code} уже существует.")
        self.wallets[currency_code] = Wallet(currency_code, 0.0)

    @classmethod
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
    
    @classmethod
    def get_wallet(self, currency_code):
        if not isinstance(currency_code, str):
            raise TypeError(type(currency_code))
        if currency_code not in self.wallets.keys():
            raise ValueError(f"Счет {currency_code} не существует.")
        return self.wallets[currency_code]

    @classmethod
    def save_to_json(self, json_name="portfolios.json"):
        json_path = DATA_DIR + '/' + json_name
        json_data = utils.load_json(json_path)
        save_location = -1
        for i in range(len(json_data)):
            if json_data[i]["user_id"] == self.user_id:
                save_location = i
                break
        if save_location < 0 and len(json_data) == 0:
            json_data.append({
                "user_id": None,
                "wallets": {}
            })
            save_location = 0
        json_data[save_location]["user_id"] = self.user_id
        wallets_dictionary = {}
        for key in self.wallets.keys():
            wallets_dictionary[key] = {
                "currency_code": self.wallets[key].currency_code,
                "balance": self.wallets[key].balance
                }
        json_data[save_location]["wallets"] = wallets_dictionary
        utils.save_json(json_path, json_data)

    @staticmethod
    def converse_to_base(current_currency, base_currency, amount):
        converse_way = current_currency + '_' + base_currency
        exchange_rates_json = utils.load_json(EXCHANGE_RATES_PATH)
        if converse_way not in exchange_rates_json.keys():
            raise ValueError(f"Курс {converse_way} не найден.")
        multiplier = exchange_rates_json[converse_way]["rate"]
        return amount * multiplier
