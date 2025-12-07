import valutatrade_hub.parser_service.config as config


class StorageUpdater:
    def __init__(self):
        cfg = config.ParserConfig()
        self.rates_path = cfg.RATES_FILE_PATH
        self.history_path = cfg.HISTORY_FILE_PATH

    @classmethod
    def save_rates(self, rates: dict):
        json_path = DATA_DIR + '/' + json_name
        json_data = utils.load_json(json_path)
        save_location = -1
        for i in range(len(json_data)):
            if json_data[i]["user_id"] == self.user_id:
                save_location = i
                break
        if save_location < 0 and len(json_data) == 0:
            json_data.append({
                "user_id": None,
                "username": None,
                "hashed_password": None,
                "salt": None,
                "registration_date": None
            })
            save_location = 0
        json_data[save_location]["user_id"] = self.user_id
        json_data[save_location]["username"] = self.username
        json_data[save_location]["hashed_password"] = self.hashed_password
        json_data[save_location]["salt"] = self.salt
        json_data[save_location]["registration_date"] = self.registration_date
        utils.save_json(json_path, json_data)

    @classmethod
    def save_history(self, history: dict):
        pass