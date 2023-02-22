import json
import requests
from conf import keys

class APIException(Exception):
    pass

class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = keys[base]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = keys[sym]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={keys[base]}&from={keys[sym]}&amount={amount}"
        payload = {}
        headers = {
            "apikey": "0Q0uyL1aEoWPWMfio4u2BuGLFNPPvFkr"
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        result = response.json()
        message = f"Цена {amount} {base} в {sym} : {[result][0]['result']}"
        return message