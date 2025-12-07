class LoggingConfig:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            print("Создание нового экземпляра LoggingConfig")
            cls.__instance = super().__new__(cls)
        else:
            print("Возврат существующего экземпляра LoggingConfig")
        return cls.__instance
    
    def __init__(self, arg1):
        print(f"Инициализация LoggingConfig")
    
    def get(key):
        match key:
            case "DATAPATH":
                pass
    
    def reload():
        pass
