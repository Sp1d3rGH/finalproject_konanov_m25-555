def InsufficientFundsError(Exception):
    def __init__(self, code, available, required, message=None):
        super().__init__(message)
        self.code = code
        self.available = available
        self.required = required

    def __str__(self):
        return f"Недостаточно средств: доступно {self.available} {self.code}, требуется {self.required} {self.code}"

def CurrencyNotFoundError(Exception):
    def __init__(self, code, message=None):
        super().__init__(message)
        self.code = code

    def __str__(self):
        return f"Неизвестная валюта '{self.code}'"

def ApiRequistError(Exception):
    def __init__(self, message=None):
        super().__init__(message)

    def __str__(self):
        return f"Ошибка при обращении к внешнему API: {self.message}"
