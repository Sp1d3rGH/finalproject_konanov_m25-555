import valutatrade_hub.core.exceptions as exceptions


KNOWN_FIAT_CURRENCIES = ["USD", "EUR"]
KNOWN_CRYP_CURRENCIES = ["BTC", "ETH"]

class Currency:
    def __init__(self, name=None, code=None):
        if (isinstance(name, str) and
            isinstance(code, str)):
            pass
        else:
            raise TypeError("Некорректный тип данных для класса Currency.")
        self.name = name
        self.code = code
    
    @property
    def name(self):
        return self.name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError(type(value))
        if value == '':
            raise ValueError("Некорректный код валюты.")
        self.name = value

    @property
    def code(self):
        return self.code
    
    @code.setter
    def code(self, value):
        if not isinstance(value, str):
            raise TypeError(type(value))
        if (' ' in value or
            value != value.upper() or
            len(value) > 5 or
            len(value) < 2):
            raise ValueError("Некорректный код валюты.")
        self.code = value

    def get_display_info(self):
        print(f"{self.code} — {self.name}")

class FiatCurrency(Currency):
    def __init__(self, name=None, code=None, issuing_country=None):
        super().__init__(name, code)
        self.issuing_country = issuing_country
    
    @property
    def issuing_country(self):
        return self.issuing_country
    
    @issuing_country.setter
    def issuing_county(self, value):
        if not isinstance(value, str):
            raise TypeError(type(value))
        if value == '':
            raise ValueError("Некорректное имя страны.")
        self.issuing_country = value
    
    def get_display_info(self):
        print(f"[FIAT] {self.code} — {self.name} (Issuing: {self.issuing_country})")

class CryptoCurrency(Currency):
    def __init__(self, name=None, code=None, algorithm=None, market_cap=None):
        super().__init__(name, code)
        self.algorithm = algorithm
        self.market_cap = market_cap
    
    @property
    def algorithm(self):
        return self.algorithm
    
    @algorithm.setter
    def algorithm(self, value):
        if not isinstance(value, str):
            raise TypeError(type(value))
        if value == '':
            raise ValueError("Некорректное имя алгоритма.")

    @property
    def market_cap(self):
        return self.market_cap
    
    @market_cap.setter
    def market_cap(self, value):
        if not isinstance(value, str):
            raise TypeError(type(value))
        if value == '':
            raise ValueError("Некорректный вид капитализации.")
        self.market_cap = value
    
    def get_display_info(self):
        print(f"[CRYPTO] {self.code} — {self.name} (Algo: {self.algorithm}, MCAP: {self.market_cap})")

def get_currency(code):
    if code in KNOWN_FIAT_CURRENCIES:
        return CryptoCurrency(code)
    elif code in KNOWN_CRYP_CURRENCIES:
        return FiatCurrency(code)
    else:
        raise exceptions.CurrencyNotFoundError(code)
