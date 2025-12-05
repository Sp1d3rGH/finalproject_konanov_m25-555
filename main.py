#!/usr/bin/env python3


import os
import valutatrade_hub.cli.interface as interface

USERS_PATH = "data/users.json"
PORTFOLIOS_PATH = "data/portfolios.json"
RATES_PATH = "data/rates.json"
EXCHANGE_RATES_PATH = "data/exchange_rates.json"

def ensure_files_exist(paths):
    for filepath in paths:
        if not os.path.exists(filepath):
            print(f"Не найден файл с данными. Создание пустого файла {filepath}.")
            os.makedirs(filepath, exist_ok=True)
            with open(filepath, "w") as file:
                if "rates.json" not in filepath:
                    file.write(str(list()))
                else:
                    file.write(str(dict()))

def main():
    ensure_files_exist([USERS_PATH,
                        PORTFOLIOS_PATH,
                        RATES_PATH,
                        EXCHANGE_RATES_PATH])
    interface.run()
    return 0
