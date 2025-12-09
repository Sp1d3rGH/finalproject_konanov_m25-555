#!/usr/bin/env python3


import os
import valutatrade_hub.cli.interface as interface
import valutatrade_hub.parser_service.config as config
import valutatrade_hub.infra.settings as settings
import valutatrade_hub.logging_config as logging_config


def ensure_files_exist():
    '''
    Создает директорию data/ и необходимые файлы в ней,
    если они еще не были созданы.
    '''
    cfg = config.ParserConfig()
    params = settings.SettingsLoader()
    log_cfg = logging_config.LoggingConfig()
    datapath = params.DATAPATH
    paths = [cfg.RATES_FILE_PATH,
             cfg.HISTORY_FILE_PATH,
             params.USERS_PATH,
             params.PORTFOLIOS_PATH]
    if not os.path.exists(datapath):
        print(f"Не найдена директория с данными. Создание пустой директории {datapath}.")
        os.makedirs(datapath, exist_ok=True)
    for filepath in paths:
        if not os.path.exists(filepath):
            print(f"Не найден файл с данными. Создание пустого файла {filepath}.")
            with open(filepath, "w") as file:
                if filepath == params.USERS_PATH or filepath == params.PORTFOLIOS_PATH:
                    file.write(str(list()))
                else:
                    file.write(str(dict()))

def main():
    ensure_files_exist()
    interface.run()
    return 0
