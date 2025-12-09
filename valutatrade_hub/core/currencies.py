import valutatrade_hub.core.exceptions as exceptions
import valutatrade_hub.parser_service.config as config


class Currency:
    def __init__(self, code=None, name=None):
        if (isinstance(name, str) and
            isinstance(code, str)):
            pass
        else:
            raise TypeError("Некорректный тип данных для класса Currency.")
        self._name = name
        self._code = code
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError(type(value))
        if value == '':
            raise ValueError("Некорректный код валюты.")
        self._name = value

    @property
    def code(self):
        return self._code
    
    @code.setter
    def code(self, value):
        if not isinstance(value, str):
            raise TypeError(type(value))
        if (' ' in value or
            value != value.upper() or
            len(value) > 5 or
            len(value) < 2):
            raise ValueError("Некорректный код валюты.")
        self._code = value

    def get_display_info(self):
        print(f"{self.code} — {self.name}")

class FiatCurrency(Currency):
    def __init__(self, code=None, name=None, issuing_country=None):
        super().__init__(code, name)
        self._issuing_country = issuing_country
    
    @property
    def issuing_country(self):
        return self._issuing_country
    
    @issuing_country.setter
    def issuing_county(self, value):
        if not isinstance(value, str):
            raise TypeError(type(value))
        if value == '':
            raise ValueError("Некорректное имя страны.")
        self._issuing_country = value
    
    def get_display_info(self):
        print(f"[FIAT] {self.code} — {self.name} (Issuing: {self.issuing_country})")

class CryptoCurrency(Currency):
    def __init__(self, code=None, name=None, algorithm=None, market_cap=None):
        super().__init__(code, name)
        self._algorithm = algorithm
        self._market_cap = market_cap
    
    @property
    def algorithm(self):
        return self._algorithm
    
    @algorithm.setter
    def algorithm(self, value):
        if not isinstance(value, str):
            raise TypeError(type(value))
        if value == '':
            raise ValueError("Некорректное имя алгоритма.")
        self._algorithm = value

    @property
    def market_cap(self):
        return self._market_cap
    
    @market_cap.setter
    def market_cap(self, value):
        if not isinstance(value, str):
            raise TypeError(type(value))
        if value == '':
            raise ValueError("Некорректный вид капитализации.")
        self._market_cap = value
    
    def get_display_info(self):
        print(f"[CRYPTO] {self.code} — {self.name} (Algo: {self.algorithm}, MCAP: {self.market_cap})")

def get_currency(code):
    cfg = config.ParserConfig()
    if not isinstance(code, str):
        raise TypeError("Код валюты не задан.")
    if code in cfg.CRYPTO_CURRENCIES:
        name = cfg.CRYPTO_ID_MAP[code]
        return CryptoCurrency(code, name)
    elif code in cfg.FIAT_CURRENCIES:
        name = cfg.FIAT_ID_MAP[code]
        return FiatCurrency(code, name)
    elif code in cfg.BASE_CURRENCY:
        name = code.lower()
        return FiatCurrency(code, name)
    else:
        raise exceptions.CurrencyNotFoundError(code)
