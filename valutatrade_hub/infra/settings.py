import valutatrade_hub.core.utils as utils

class SettingsLoader:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            print("Создание нового экземпляра SettingsLoader")
            cls.__instance = super().__new__(cls)
        else:
            print("Возврат существующего экземпляра SettingsLoader")
        return cls.__instance
    
    def __init__(self):
        self.CONFIGPATH = "valutatrade_hub/infra/config.json"
        print(f"Инициализация SettingsLoader")
        config_data = utils.load_json(self.CONFIGPATH)
        self.DATAPATH = config_data["DATAPATH"]
        self.RATES_TTL_SECONDS = int(config_data["RATES_TTL_SECONDS"])
        self.DEFAULT_CURRENCY = config_data["DEFAULT_CURRENCY"]
        self.LOGS_PATH = config_data["LOGS_PATH"]
        self.USERS_PATH = config_data["USERS_PATH"]
        self.PORTFOLIOS_PATH = config_data["PORTFOLIOS_PATH"]
        self.SALT_LENGTH = config_data["SALT_LENGTH"]
    
    def reload(self):
        config_data = utils.load_json(self.CONFIGPATH)
        self.DATAPATH = config_data["DATAPATH"]
        self.RATES_TTL_SECONDS = int(config_data["RATES_TTL_SECONDS"])
        self.DEFAULT_CURRENCY = config_data["DEFAULT_CURRENCY"]
        self.LOGS_PATH = config_data["LOGS_PATH"]
        self.USERS_PATH = config_data["USERS_PATH"]
        self.PORTFOLIOS_PATH = config_data["PORTFOLIOS_PATH"]
        self.SALT_LENGTH = config_data["SALT_LENGTH"]
