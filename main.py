import random
import time
from typing import List, Dict
import hmac
import hashlib
import requests
from urllib.parse import urlencode


def create_orders(data: Dict) -> List[Dict]:
    # Создаем пустой список для хранения ордеров
    orders = []
    # Вычисляем объем каждого ордера
    volume_per_order = data['volume'] / data['number']
    # Создаем нужное количество ордеров
    for i in range(data['number']):
        # Создаем словарь для хранения информации об ордере
        order = {}
        # Задаем сторону торговли
        order['side'] = data['side']
        # Выбираем случайную цену в заданном диапазоне и округляем до одного знака после запятой
        order['price'] = round(random.uniform(data['priceMin'], data['priceMax']), 1)
        # Выбираем случайный объем в заданном диапазоне
        volume = random.uniform(volume_per_order - data['amountDif'], volume_per_order + data['amountDif'])
        # Вычисляем объем в покупаемой валюте и округляем до трех знаков после запятой
        order['volume'] = round(volume / order['price'], 3)
        # Добавляем ордер в список
        orders.append(order)
    # Возвращаем список ордеров
    # print("Orders: ", orders)
    return orders


def create_order_on_binance(api_key, api_secret, order):
    try:
        ###
        # Блок с получением времени сервера для большей надежности кода,
        # чтобы работа не зависила от времени на локальной машине с которой запускается код

        # URL для получения времени сервера Binance
        url = 'https://api.binance.com/api/v3/time'

        # Отправляем GET-запрос к API Binance
        response = requests.get(url)
        response.raise_for_status()

        # Получаем время сервера Binance из ответа
        server_time = response.json()
        timestamp = server_time['serverTime']
        ###

        base_url = 'https://testnet.binancefuture.com'
        endpoint = '/fapi/v1/order'
        params = {
            'symbol': 'BTCUSDT',
            'side': order['side'],
            'type': 'LIMIT',
            'timeInForce': 'GTC',
            'quantity': order['volume'],
            'price': order['price'],
            'recvWindow': 5000,
            # Для большей надежности кода, чтобы работа не зависила от времени на локальной машине с которой запускается код
            'timestamp': timestamp # int(time.time() * 1000)
        }

        query_string = urlencode(params)
        signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = f"{base_url}{endpoint}?{query_string}&signature={signature}"

        headers = {
            'X-MBX-APIKEY': api_key
        }

        response = requests.post(url, headers=headers)
        # print("Response: ", response.json())
        return response
    except Exception as e:
        # Ошибки
        print(f'Error creating order: {e}')
        return f'Error creating order: {e}'


# Замените эти значения на свои ключи API и секретный ключ
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'

# # Данные от фронтенда
# data = {
#    "volume": 5000.0,  # Объем в долларах
#    "number": 5,  # На сколько ордеров нужно разбить этот объем
#    "amountDif": 50.0,  # Разброс в долларах, в пределах которого случайным образом выбирается объем в верхнюю и нижнюю сторону
#    "side": "BUY",  # Сторона торговли (SELL или BUY)
#    "priceMin": 26500.0,  # Нижний диапазон цены, в пределах которого нужно случайным образом выбрать цену
#    "priceMax": 27000.0  # Верхний диапазон цены, в пределах которого нужно случайным образом выбрать цену
# }
#
# # Создаем ордера с помощью функции create_orders
# orders = create_orders(data)
#
# # Отправляем созданные ордера на биржу Binance с обработкой ошибок
# for order in orders:
#     create_order_on_binance(api_key, api_secret, order)
