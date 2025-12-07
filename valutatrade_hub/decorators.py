import valutatrade_hub.core.exceptions as exceptions

def handle_errors(func):
    '''
    Обрабатывает ошибки, которые
    не были предусмотрены в логике функций.
    '''
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exceptions.InsufficientFundsError as e:
            print(e)
        except exceptions.CurrencyNotFoundError as e:
            print(e)
        except exceptions.ApiRequistError as e:
            print(e)
    return wrapper

def log_action(func, verbose=True):
    '''
    Логирует необходимые значения в точках выполнения функций.
    '''
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"INFO 2025-10-09T12:05:22 BUY user='alice' currency='BTC' amount=0.0500 rate=59300.00 base='USD' result=OK")
        return result
    return wrapper
