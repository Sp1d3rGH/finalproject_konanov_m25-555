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
