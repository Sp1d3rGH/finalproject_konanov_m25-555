import shlex
import valutatrade_hub.core.usecases as usecases


def run():
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
                usecases.login_user(input_name, input_pass)
            case "show-portfolio":
                usecases.show_portfolio()
            case "buy":
                pass
            case "sell":
                pass
            case "get-rate":
                pass
            case "help":
                pass
            case "exit":
                return None
            case _:
                print(f"Команды '{user_args[0]}' нет. Попробуйте снова.")
