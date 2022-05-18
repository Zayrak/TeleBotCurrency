import json
import requests

from Config import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = keys[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество валюты!')

        r = requests.get(f"https://free.currconv.com/api/v7/convert?q={base_key}_{sym_key}&compact=ultra&apiKey=18622d5dd3596f48a434")
        resp = json.loads(r.content)
        key = list(resp.keys())
        new_price = float(resp[key[0]]) * amount
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {sym} : {new_price}"
        return message
