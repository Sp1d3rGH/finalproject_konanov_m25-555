# Сервис ValutaTrade Hub

Проект реализует сервис хранения и обмена валютами.
Данные курсов берутся из публичных API [CoinGecko](www.coingecko.com) и [ExchangeRate](exchangerate-api.com).
Пользователь может смотреть обменные курсы валют, покупать, продавать и хранить их в кошельке.

Поддерживаемые валюты: `USD`, `EUR`, `RUB`, `GBP`, `BTC`, `SOL`, `ETH`.

## Требования к установке

* **Python** от 3.13;
* **Poetry** от 2.0.0 до 3.0.0;
* **Ruff** от 0.14.7;
* **Requests** от 2.32.5 до 3.0.0;
* **Prettytable** от 3.17.0 до 4.0.0

и/или

* **GNU Make**.

## Установка

Для начала зарегистрируйтесь на сайте [exchangerate-api.com](exchangerate-api.com) и получите ключ к API.

---

Распакуйте проект в удобную директорию. После выполнения требований введите в установленной директории:
```
make install
```
или
```
poetry install
```

---

Задайте переменную среды:
```
export EXCHANGERATE_API_KEY="api_key"
```
где `"api_key"` - это ваш ключ к API.

---

После успешной установки можно начать пользоваться:
```
make run
```
или
```
poetry run valutatrade
```

# Asciinema
https://asciinema.org/a/aDInJWudMc3BhVhBb8YCe1TQx