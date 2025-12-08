import valutatrade_hub.parser_service.config as config
import valutatrade_hub.core.utils as utils


class StorageUpdater:
    def __init__(self):
        self.cfg = config.ParserConfig()
    
    def save_rates(self, rates: dict):
        json_data = utils.load_json(self.cfg.RATES_FILE_PATH)
        for key, value in rates["pairs"]:
            json_data["pairs"][key] = value
        json_data["last_refresh"] = rates["last_refresh"]
        utils.save_json(self.cfg.RATES_FILE_PATH, json_data)

    def save_history(self, history_entry: dict):
        json_data = utils.load_json(self.cfg.HISTORY_FILE_PATH)
        for key, value in history_entry:
            if key in json_data.keys():
                raise ValueError("Такая запись в истории уже существует.")
            json_data.update({key: value})
        utils.save_json(self.cfg.HISTORY_FILE_PATH)
