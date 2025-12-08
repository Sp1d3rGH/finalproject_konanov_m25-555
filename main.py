#!/usr/bin/env python3


import os
import valutatrade_hub.cli.interface as interface
import valutatrade_hub.parser_service.config as config
import valutatrade_hub.infra.settings as settings
import valutatrade_hub.logging_config as logging_config


def ensure_files_exist():
    cfg = config.ParserConfig()
    params = settings.SettingsLoader()
    log_cfg = logging_config.LoggingConfig()
    paths = [cfg.RATES_FILE_PATH,
             cfg.HISTORY_FILE_PATH,
             params.USERS_PATH,
             params.PORTFOLIOS_PATH,
             log_cfg.LOGS_PATH]
    for filepath in paths:
        if not os.path.exists(filepath):
            print(f"Не найден файл с данными. Создание пустого файла {filepath}.")
            os.makedirs(filepath, exist_ok=True)
            with open(filepath, "w") as file:
                if "rates.json" in filepath:
                    file.write(str(dict()))
                elif "rates.json" not in filepath:
                    file.write(str(list()))
                elif ".log" in filepath:
                    file.write('')

def main():
    ensure_files_exist()
    interface.run()
    return 0
