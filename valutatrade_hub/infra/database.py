class DatabaseManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            print("Создание нового экземпляра DatabaseManager")
            cls.__instance = super().__new__(cls)
        else:
            pass
            print("Возврат существующего экземпляра DatabaseManager")
        return cls.__instance

    def __init__(self):
        print("Инициализация DatabaseManager")
