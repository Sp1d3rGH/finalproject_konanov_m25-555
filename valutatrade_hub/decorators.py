import os
import glob
import datetime
import valutatrade_hub.core.exceptions as exceptions
import valutatrade_hub.logging_config as logging_config

def handle_errors(func):
    '''
    Обрабатывает ошибки, которые
    не были предусмотрены в логике функций.
    '''
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError as e:
            print(f"Ошибка типизации: {e}")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except IOError as e:
            print(f"Ошибка ввода: {e}")
        except exceptions.InsufficientFundsError as e:
            print(f"Недостаточно средств: {e}")
        except exceptions.CurrencyNotFoundError as e:
            print(f"Некорректная валюта: {e}")
        except exceptions.ApiRequestError as e:
            print(f"Ошибка доспупа к API: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
    return wrapper

def log_action(verbose=True):
    def log_action_decorator(func):
        '''
        Логирует необходимые значения в точках выполнения функций.
        '''
        def wrapper(*args, **kwargs):
            '''
            Просматриваем файлы "logs/actions*.log".
            Если найден лог, созданный не позже чем за
            LOGS_RESET_TIME от настоящего времени,
            пишем в него, иначе создаем новый.
            '''
            log_cfg = logging_config.LoggingConfig()
            if not os.path.exists(log_cfg.LOGS_DIR):
                print(f"Создание директории с логами {log_cfg.LOGS_DIR}.")
                os.makedirs(log_cfg.LOGS_DIR, exist_ok=True)
            log_date = datetime.datetime.now()
            last_date = datetime.datetime.min
            for filename in glob.glob(log_cfg.LOGS_DIR + '/' + log_cfg.LOGS_NAME + '*' + log_cfg.LOGS_FORMAT):
                filename.find(log_cfg.LOGS_NAME)
                file_date = filename[filename.find(log_cfg.LOGS_NAME) + len(log_cfg.LOGS_NAME):filename.find(log_cfg.LOGS_FORMAT)]
                file_date = datetime.datetime.strptime(file_date, "%Y-%m-%d %H:%M:%S")
                if file_date > last_date:
                    last_date = file_date
            log_time_diff = log_date - last_date
            if log_time_diff > log_cfg.LOGS_RESET_TIME:
                # Пишем в новый лог
                filepath = log_cfg.LOGS_DIR + '/' + log_cfg.LOGS_NAME + log_date.strftime("%Y-%m-%d %H:%M:%S") + log_cfg.LOGS_FORMAT
                log_entry = log_cfg.LOGS_LEVEL + ' ' + log_date.strftime("%Y-%m-%d %H:%M:%S") + ' '
                try:
                    result = func(*args, **kwargs)
                    logging_data = result[1]
                    log_entry += (logging_data["operation"] +
                                    " user=" + logging_data["user"] +
                                    " currency=" + logging_data["currency"] +
                                    " amount=" + str(logging_data["amount"]) + 
                                    " rate=" + str(logging_data["rate"]) + 
                                    " base=" + logging_data["base"])
                    if verbose:
                        if logging_data["operation"] == "BUY" or logging_data["operation"] == "SELL":
                            log_entry += (" - BALANCE BEFORE OPERATION " + str(logging_data["was_amount"]) +
                                            " AFTER " + str(logging_data["was_amount"] + logging_data["amount"]) + " -")
                    log_entry += " result=OK\n"
                    # print(f"Создание нового лога {filepath}.")
                    with open(filepath, "w") as file:
                        file.write(log_entry)
                except TypeError as e:
                    log_entry += "ERROR Ошибка типизации: " + str(e) + "\n"
                    # print(f"Создание нового лога {filepath}.")
                    with open(filepath, "w") as file:
                        file.write(log_entry)
                    raise e
                except ValueError as e:
                    log_entry += "ERROR Ошибка валидации: " + str(e) + "\n"
                    # print(f"Создание нового лога {filepath}.")
                    with open(filepath, "w") as file:
                        file.write(log_entry)
                    raise e
                except exceptions.CurrencyNotFoundError as e:
                    log_entry += "ERROR Неизвестная валюта: " + str(e) + "\n"
                    # print(f"Создание нового лога {filepath}.")
                    with open(filepath, "w") as file:
                        file.write(log_entry)
                    raise e
                except exceptions.InsufficientFundsError as e:
                    log_entry += "ERROR Недостаточно средств: " + str(e) + "\n"
                    # print(f"Создание нового лога {filepath}.")
                    with open(filepath, "w") as file:
                        file.write(log_entry)
                    raise e
            else:
                # Пишем в существующий
                filepath = log_cfg.LOGS_DIR + '/' + log_cfg.LOGS_NAME + last_date.strftime("%Y-%m-%d %H:%M:%S") + log_cfg.LOGS_FORMAT
                log_entry = log_cfg.LOGS_LEVEL + ' ' + log_date.strftime("%Y-%m-%d %H:%M:%S") + ' '
                try:
                    result = func(*args, **kwargs)
                    logging_data = result[1]
                    log_entry += (logging_data["operation"] +
                                    " user=" + logging_data["user"] +
                                    " currency=" + logging_data["currency"] +
                                    " amount=" + str(logging_data["amount"]) + 
                                    " rate=" + str(logging_data["rate"]) + 
                                    " base=" + logging_data["base"])
                    if verbose:
                        if logging_data["operation"] == "BUY" or logging_data["operation"] == "SELL":
                            log_entry += (" - BALANCE BEFORE OPERATION " + str(logging_data["was_amount"]) +
                                            " AFTER " + str(logging_data["was_amount"] + logging_data["amount"]) + " -")
                    log_entry += " result=OK\n"
                    # print(f"Запись в старый лог {filepath}.")
                    with open(filepath, "a") as file:
                        file.write(log_entry)
                except TypeError as e:
                    log_entry += "ERROR Ошибка типизации: " + str(e) + "\n"
                    # print(f"Запись в старый лог {filepath}.")
                    with open(filepath, "a") as file:
                        file.write(log_entry)
                    raise e
                except ValueError as e:
                    log_entry += "ERROR Ошибка валидации: " + str(e) + "\n"
                    # print(f"Запись в старый лог {filepath}.")
                    with open(filepath, "a") as file:
                        file.write(log_entry)
                    raise e
                except exceptions.CurrencyNotFoundError as e:
                    log_entry += "ERROR Неизвестная валюта: " + str(e) + "\n"
                    # print(f"Запись в старый лог {filepath}.")
                    with open(filepath, "a") as file:
                        file.write(log_entry)
                    raise e
                except exceptions.InsufficientFundsError as e:
                    log_entry += "ERROR Недостаточно средств: " + str(e) + "\n"
                    # print(f"Запись в старый лог {filepath}.")
                    with open(filepath, "a") as file:
                        file.write(log_entry)
                    raise e
            return result
        return wrapper
    return log_action_decorator
