import shlex
import valutatrade_hub.core.usecases as usecases


def run():
    current_user = None
    while True:
        print("> ", end='')
        user_input = str(input())
        user_args = shlex.split(user_input)
        if not user_args:
            continue
        match user_args[0]:
            case "register":
                input_name = None
                input_pass = None
                special_args = ["--username", "--password"]
                for i in range(1, len(user_args)):
                    if i % 2 == 0 and user_args[i-1] not in special_args:
                        raise IOError("Ошибка синтаксиса:", user_args[i-1], user_args[i])
                    elif user_args[i-1] in special_args and user_args[i] not in special_args:
                        match user_args[i-1]:
                            case "--username":
                                input_name = user_args[i]
                                special_args.remove("--username")
                            case "--password":
                                input_pass = user_args[i]
                                special_args.remove("--password")
                    elif user_args[i-1] in special_args and user_args[i] in special_args:
                        raise IOError("Ошибка синтаксиса:", user_args[i-1], user_args[i])
                usecases.register_user(input_name, input_pass)
                print(f"Пользователь '{input_name}' зарегистрирован. Войдите: "
                      f"login --username {input_name} "
                      f"--password {'*' * len(input_pass)}")
            case "login":
                input_name = None
                input_pass = None
                special_args = ["--username", "--password"]
                for i in range(1, len(user_args)):
                    if i % 2 == 0 and user_args[i-1] not in special_args:
                        raise IOError("Ошибка синтаксиса:", user_args[i-1], user_args[i])
                    elif user_args[i-1] in special_args and user_args[i] not in special_args:
                        match user_args[i-1]:
                            case "--username":
                                input_name = user_args[i]
                                special_args.remove("--username")
                            case "--password":
                                input_pass = user_args[i]
                                special_args.remove("--password")
                    elif user_args[i-1] in special_args and user_args[i] in special_args:
                        raise IOError("Ошибка синтаксиса:", user_args[i-1], user_args[i])
                current_user = usecases.login_user(input_name, input_pass)
            case "show-portfolio":
                if not current_user:
                    raise ValueError("Для выполнения этой команды необходимо войти в аккаунт.")
                input_currency = "USD"
                special_args = ["--base"]
                for i in range(1, len(user_args)):
                    if i % 2 == 0 and user_args[i-1] not in special_args:
                        raise IOError("Ошибка синтаксиса:", user_args[i-1], user_args[i])
                    elif user_args[i-1] in special_args and user_args[i] not in special_args:
                        match user_args[i-1]:
                            case "--base":
                                input_currency = user_args[i]
                                special_args.remove("--base")
                    elif user_args[i-1] in special_args and user_args[i] in special_args:
                        raise IOError("Ошибка синтаксиса:", user_args[i-1], user_args[i])
                usecases.show_portfolio(input_currency, current_user)
            case "buy":
                if not current_user:
                    raise ValueError("Для выполнения этой команды необходимо войти в аккаунт.")
                input_currency = None
                input_amount = None
                special_args = ["--currency", "--amount"]
                for i in range(1, len(user_args)):
                    if i % 2 == 0 and user_args[i-1] not in special_args:
                        raise IOError("Ошибка синтаксиса:", user_args[i-1], user_args[i])
                    elif user_args[i-1] in special_args and user_args[i] not in special_args:
                        match user_args[i-1]:
                            case "--currency":
                                input_currency = user_args[i]
                                special_args.remove("--currency")
                            case "--amount":
                                input_amount = user_args[i]
                                special_args.remove("--amount")
                    elif user_args[i-1] in special_args and user_args[i] in special_args:
                        raise IOError("Ошибка синтаксиса:", user_args[i-1], user_args[i])
                usecases.buy_by_user(input_currency, input_amount, current_user)
            case "sell":
                if not current_user:
                    raise ValueError("Для выполнения этой команды необходимо войти в аккаунт.")
                input_currency = None
                input_amount = None
                special_args = ["--currency", "--amount"]
                for i in range(1, len(user_args)):
                    if i % 2 == 0 and user_args[i-1] not in special_args:
                        raise IOError("Ошибка синтаксиса:", user_args[i-1], user_args[i])
                    elif user_args[i-1] in special_args and user_args[i] not in special_args:
                        match user_args[i-1]:
                            case "--currency":
                                input_currency = user_args[i]
                                special_args.remove("--currency")
                            case "--amount":
                                input_amount = user_args[i]
                                special_args.remove("--amount")
                    elif user_args[i-1] in special_args and user_args[i] in special_args:
                        raise IOError("Ошибка синтаксиса:", user_args[i-1], user_args[i])
                usecases.sell_by_user(input_currency, input_amount, current_user)
            case "get-rate":
                input_base = None
                input_pref = None
                special_args = ["--from", "--to"]
                for i in range(1, len(user_args)):
                    if i % 2 == 0 and user_args[i-1] not in special_args:
                        raise IOError("Ошибка синтаксиса:", user_args[i-1], user_args[i])
                    elif user_args[i-1] in special_args and user_args[i] not in special_args:
                        match user_args[i-1]:
                            case "--from":
                                input_base = user_args[i]
                                special_args.remove("--from")
                            case "--to":
                                input_pref = user_args[i]
                                special_args.remove("--to")
                    elif user_args[i-1] in special_args and user_args[i] in special_args:
                        raise IOError("Ошибка синтаксиса:", user_args[i-1], user_args[i])
                usecases.get_rate_user(input_base, input_pref)
            case "help":
                usecases.show_help()
            case "exit":
                return None
            case _:
                print(f"Команды '{user_args[0]}' нет. Попробуйте снова.")
