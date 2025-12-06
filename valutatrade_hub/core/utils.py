import json


def load_json(filepath):
    with open(filepath) as f:
        data = json.load(f)
        if "rates.json" not in filepath:
            if not isinstance(data, list):
                raise TypeError(f"Некорректный формат файла {filepath}.")
        else:
            if not isinstance(data, dict):
                raise TypeError(f"Некорректный формат файла {filepath}.")
        print(f"Успешное чтение из файла {filepath}.")
        return data

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        if "rates.json" not in filepath:
            if not isinstance(data, list):
                raise TypeError(f"Некорректный формат для записи в файл: {type(data)}.")
        else:
            if not isinstance(data, dict):
                raise TypeError(f"Некорректный формат для записи в файл: {type(data)}.")
        json.dump(data, f)
        print(f"Успешная запись в файл {filepath}.")

def parse_values(values, pref_types):
    '''
    На вход:
    ['123', ...], ['int', ...]
    На выход:
    [123, ...]
    '''
    if not isinstance(values, list):
        values = [values]
    if not isinstance(pref_types, list):
        pref_types = [pref_types]
    if len(values) != len(pref_types):
        raise ValueError(f"Длины списков не сходятся: {values}, {pref_types}.")
    parsed_values = []
    for i in range(len(values)):
        match pref_types[i]:
            case "int":
                try:
                    parsed_values.append(int(values[i]))
                except ValueError:
                    raise ValueError(f"Нельзя привести {values[i]} к {pref_types[i]}.")
            case "float":
                try:
                    parsed_values.append(float(values[i]))
                except ValueError:
                    raise ValueError(f"Нельзя привести {values[i]} к {pref_types[i]}.")
            case "bool":
                if values[i].lower() == "true":
                    parsed_values.append(True)
                elif values[i].lower() == "false":
                    parsed_values.append(False)
                else:
                    raise ValueError(f"Нельзя привести {values[i]} к {pref_types[i]}.")
            case "str":
                parsed_values.append(str(values[i]))
    return parsed_values
