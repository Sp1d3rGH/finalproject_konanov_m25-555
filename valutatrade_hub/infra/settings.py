class SettingsLoader:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            print("Создание нового экземпляра SettingsLoader")
            cls.__instance = super().__new__(cls)
        else:
            print("Возврат существующего экземпляра SettingsLoader")
        return cls.__instance
    
    def __init__(self, DATAPATH, RATES_TTL_SECONDS, DEFAULT_CURRENCY, LOGS_PATH):
        print(f"Инициализация SettingsLoader")
    
    def get(key):
        match key:
            case "DATAPATH":
                pass
    
    def reload():
        pass
