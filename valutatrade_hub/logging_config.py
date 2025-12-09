import datetime


class LoggingConfig:
    '''
    - LOGS_DIR - директория с логами.
    - LOGS_NAME - базовое имя файла с логами.
    - LOGS_FORMAT - формат файла с логами.
    - LOGS_LEVEL - уровень логирования.
    - LOGS_RESET_TIME - ротация логов (в часах).
    Если разница между текущим временем и временем создания
    последнего файла с логами будет превосходить LOGS_RESET_TIME,
    то логи будут записываться в новый файл.
    '''
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            # print("Создание нового экземпляра LoggingConfig")
            cls.__instance = super().__new__(cls)
        else:
            pass
            # print("Возврат существующего экземпляра LoggingConfig")
        return cls.__instance

    def __init__(self,
                 LOGS_DIR = "logs",
                 LOGS_NAME = "actions",
                 LOGS_FORMAT = ".log",
                 LOGS_LEVEL = "INFO",
                 LOGS_RESET_TIME = datetime.timedelta(hours=0.05)):
        self.LOGS_DIR = LOGS_DIR
        self.LOGS_NAME = LOGS_NAME
        self.LOGS_FORMAT = LOGS_FORMAT
        self.LOGS_LEVEL = LOGS_LEVEL
        self.LOGS_RESET_TIME = LOGS_RESET_TIME
