import shlex

import valutatrade_hub.core.usecases as usecases
import valutatrade_hub.decorators as decorators
import valutatrade_hub.infra.settings as settings
import valutatrade_hub.parser_service.api_clients as api_clients
import valutatrade_hub.parser_service.config as config
import valutatrade_hub.parser_service.storage as storage
import valutatrade_hub.parser_service.updater as updater


def run():
    params = settings.SettingsLoader()
    cfg = config.ParserConfig()
    current_user = None
    exit_call = None
    usecases.show_help()
    while not exit_call:
        print("\n> ", end='')
        user_input = str(input())
        user_args = shlex.split(user_input)
        if not user_args:
            continue
        else:
            action_user = None
            loop_result = run_loop(current_user, user_args, params, cfg)
            if loop_result:
                action_user, exit_call = loop_result
            if action_user:
                current_user = action_user

@decorators.handle_errors
def run_loop(current_user, user_args, params, cfg):
    match user_args[0]:
        case "register":
            input_name = None
            input_pass = None
            special_args = ["--username", "--password"]
            for i in range(1, len(user_args)):
                if i % 2 == 0 and user_args[i-1] not in special_args:
                    raise IOError(user_args[i-1] + ' ' + user_args[i] + ". "
                                  "Чтобы получить справку, вызовите 'help'.")
                elif (user_args[i-1] in special_args and
                      user_args[i] not in special_args):
                    match user_args[i-1]:
                        case "--username":
                            input_name = user_args[i]
                            special_args.remove("--username")
                        case "--password":
                            input_pass = user_args[i]
                            special_args.remove("--password")
                elif user_args[i-1] in special_args and user_args[i] in special_args:
                    raise IOError(user_args[i-1] + ' ' + user_args[i] + ". "
                                  "Чтобы получить справку, вызовите 'help'.")
            usecases.register_user(input_name, input_pass)
            print(f"Пользователь '{input_name}' зарегистрирован. Войдите: "
                    f"login --username {input_name} "
                    f"--password {'*' * len(input_pass)}")
            return None, None
        case "login":
            input_name = None
            input_pass = None
            special_args = ["--username", "--password"]
            for i in range(1, len(user_args)):
                if i % 2 == 0 and user_args[i-1] not in special_args:
                    raise IOError(user_args[i-1] + ' ' + user_args[i] + ". "
                                  "Чтобы получить справку, вызовите 'help'.")
                elif (user_args[i-1] in special_args and
                      user_args[i] not in special_args):
                    match user_args[i-1]:
                        case "--username":
                            input_name = user_args[i]
                            special_args.remove("--username")
                        case "--password":
                            input_pass = user_args[i]
                            special_args.remove("--password")
                elif user_args[i-1] in special_args and user_args[i] in special_args:
                    raise IOError(user_args[i-1] + ' ' + user_args[i] + ". "
                                  "Чтобы получить справку, вызовите 'help'.")
            current_user = usecases.login_user(input_name, input_pass)[0]
            return current_user, None
        case "show-portfolio":
            if not current_user:
                raise ValueError("Для выполнения этой команды "
                                 "необходимо войти в аккаунт.")
            input_currency = cfg.BASE_CURRENCY
            special_args = ["--base"]
            for i in range(1, len(user_args)):
                if i % 2 == 0 and user_args[i-1] not in special_args:
                    raise IOError(user_args[i-1] + ' ' + user_args[i] + ". "
                                  "Чтобы получить справку, вызовите 'help'.")
                elif (user_args[i-1] in special_args and
                      user_args[i] not in special_args):
                    match user_args[i-1]:
                        case "--base":
                            input_currency = user_args[i]
                            special_args.remove("--base")
                elif user_args[i-1] in special_args and user_args[i] in special_args:
                    raise IOError(user_args[i-1] + ' ' + user_args[i] + ". "
                                  "Чтобы получить справку, вызовите 'help'.")
            usecases.show_portfolio(input_currency, current_user)
            return None, None
        case "buy":
            if not current_user:
                raise ValueError("Для выполнения этой команды "
                                 "необходимо войти в аккаунт.")
            input_currency = None
            input_amount = None
            special_args = ["--currency", "--amount"]
            for i in range(1, len(user_args)):
                if i % 2 == 0 and user_args[i-1] not in special_args:
                    raise IOError(user_args[i-1] + ' ' + user_args[i] + ". "
                                  "Чтобы получить справку, вызовите 'help'.")
                elif (user_args[i-1] in special_args and
                      user_args[i] not in special_args):
                    match user_args[i-1]:
                        case "--currency":
                            input_currency = user_args[i]
                            special_args.remove("--currency")
                        case "--amount":
                            input_amount = user_args[i]
                            special_args.remove("--amount")
                elif user_args[i-1] in special_args and user_args[i] in special_args:
                    raise IOError(user_args[i-1] + ' ' + user_args[i] + ". "
                                  "Чтобы получить справку, вызовите 'help'.")
            usecases.buy_by_user(input_currency, input_amount, current_user)
            return None, None
        case "sell":
            if not current_user:
                raise ValueError("Для выполнения этой команды "
                                 "необходимо войти в аккаунт.")
            input_currency = None
            input_amount = None
            special_args = ["--currency", "--amount"]
            for i in range(1, len(user_args)):
                if i % 2 == 0 and user_args[i-1] not in special_args:
                    raise IOError(user_args[i-1] + ' ' + user_args[i] + ". "
                                  "Чтобы получить справку, вызовите 'help'.")
                elif (user_args[i-1] in special_args and
                      user_args[i] not in special_args):
                    match user_args[i-1]:
                        case "--currency":
                            input_currency = user_args[i]
                            special_args.remove("--currency")
                        case "--amount":
                            input_amount = user_args[i]
                            special_args.remove("--amount")
                elif user_args[i-1] in special_args and user_args[i] in special_args:
                    raise IOError(user_args[i-1] + ' ' + user_args[i] + ". "
                                  "Чтобы получить справку, вызовите 'help'.")
            usecases.sell_by_user(input_currency, input_amount, current_user)
            return None, None
        case "get-rate":
            input_base = None
            input_pref = None
            special_args = ["--from", "--to"]
            for i in range(1, len(user_args)):
                if i % 2 == 0 and user_args[i-1] not in special_args:
                    raise IOError(user_args[i-1] + ' ' + user_args[i] + ". "
                                  "Чтобы получить справку, вызовите 'help'.")
                elif (user_args[i-1] in special_args and
                      user_args[i] not in special_args):
                    match user_args[i-1]:
                        case "--from":
                            input_base = user_args[i]
                            special_args.remove("--from")
                        case "--to":
                            input_pref = user_args[i]
                            special_args.remove("--to")
                elif user_args[i-1] in special_args and user_args[i] in special_args:
                    raise IOError(user_args[i-1] + ' ' + user_args[i] + ". "
                                  "Чтобы получить справку, вызовите 'help'.")
            usecases.get_rate_user(input_base, input_pref)
            return None, None
        case "update-rates":
            input_source = ''
            special_args = ["--source"]
            for i in range(1, len(user_args)):
                if i % 2 == 0 and user_args[i-1] not in special_args:
                    raise IOError(user_args[i-1] + ' ' + user_args[i] + ". "
                                  "Чтобы получить справку, вызовите 'help'.")
                elif (user_args[i-1] in special_args and
                      user_args[i] not in special_args):
                    match user_args[i-1]:
                        case "--source":
                            input_source = user_args[i]
                            special_args.remove("--source")
                elif user_args[i-1] in special_args and user_args[i] in special_args:
                    raise IOError(user_args[i-1] + ' ' + user_args[i] + ". "
                                  "Чтобы получить справку, вызовите 'help'.")
            crypto_service = api_clients.CoinGeckoClient()
            fiat_service = api_clients.ExchangeRateApiClient()
            storage_service = storage.StorageUpdater()
            updater_service = updater.RatesUpdater(
                crypto_service, fiat_service, storage_service, input_source)
            updater_service.run_update()
            return None, None
        case "show-rates":
            input_currency = None
            input_top = None
            input_base = None
            special_args = ["--currency", "--top", "--base"]
            for i in range(1, len(user_args)):
                if i % 2 == 0 and user_args[i-1] not in special_args:
                    raise IOError(user_args[i-1] + ' ' + user_args[i] + ". "
                                  "Чтобы получить справку, вызовите 'help'.")
                elif (user_args[i-1] in special_args and
                      user_args[i] not in special_args):
                    match user_args[i-1]:
                        case "--currency":
                            input_currency = user_args[i]
                            special_args.remove("--currency")
                        case "--top":
                            input_top = user_args[i]
                            special_args.remove("--top")
                        case "--base":
                            input_base = user_args[i]
                            special_args.remove("--base")
                elif (user_args[i-1] in special_args and
                      user_args[i] in special_args):
                    raise IOError(user_args[i-1] + ' ' + user_args[i] + ". "
                                  "Чтобы получить справку, вызовите 'help'.")
            usecases.show_rates_user(input_currency, input_top, input_base)
            return None, None
        case "help":
            usecases.show_help()
            return None, None
        case "exit":
            return None, "exit"
        case _:
            raise IOError(f"Команды '{user_args[0]}' нет. "
                          f"Чтобы получить справку, вызовите 'help'.")
