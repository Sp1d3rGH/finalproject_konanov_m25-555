class InsufficientFundsError(Exception):
    def __init__(self, code, available, required, message=None):
        super().__init__(message)
        self.code = code
        self.available = available
        self.required = required

    def __str__(self):
        return (f"Доступно {self.available} {self.code}, "
                f"требуется {self.required} {self.code}")

class CurrencyNotFoundError(Exception):
    def __init__(self, code, message=None):
        super().__init__(message)
        self.code = code

    def __str__(self):
        return f"Неизвестная валюта '{self.code}'"

class ApiRequestError(Exception):
    def __init__(self, code, message=None):
        super().__init__(message)
        self.code = code

    def __str__(self):
        return f"Ошибка при обращении к внешнему API: {self.code}"
