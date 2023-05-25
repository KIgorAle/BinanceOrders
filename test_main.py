import unittest

from main import create_orders, create_order_on_binance, api_key, api_secret


class TestCreateOrderOnBinance(unittest.TestCase):
    def test_create_order_on_binance_with_create_orders(self):
        # Данные для создания ордеров
        data = {
            "volume": 5000.0,  # Объем в долларах
            "number": 5,  # На сколько ордеров нужно разбить этот объем
            "amountDif": 50.0, # Разброс в долларах, в пределах которого случайным образом выбирается объем в верхнюю и нижнюю сторону
            "side": "BUY",  # Сторона торговли (SELL или BUY)
            "priceMin": 26500.0,  # Нижний диапазон цены, в пределах которого нужно случайным образом выбрать цену
            "priceMax": 27000.0  # Верхний диапазон цены, в пределах которого нужно случайным образом выбрать цену
        }
        # Создаем ордера с помощью функции create_orders
        orders = create_orders(data)
        # Проверяем, что количество ордеров соответствует заданному числу
        self.assertEqual(len(orders), data['number'])
        # Проверяем, что общий объем ордеров соответствует заданному объему
        total_volume = sum(order['volume']*order['price'] for order in orders)
        self.assertAlmostEqual(total_volume, data['volume'], delta=data['amountDif']*data['number'])
        # Проверяем каждый ордер
        for order in orders:
            # Тест create_orders
            # Проверяем, что сторона торговли соответствует заданной стороне
            self.assertEqual(order['side'], data['side'])
            # Проверяем, что цена находится в заданном диапазоне
            self.assertGreaterEqual(order['price'], data['priceMin'])
            self.assertLessEqual(order['price'], data['priceMax'])

            # Тест create_order_on_binance
            result = create_order_on_binance(api_key, api_secret, order)
            r_json = result.json()
            # Проверяем, что функция возвращает ожидаемый результат
            self.assertEqual(result.status_code, 200)
            self.assertEqual(r_json['symbol'], 'BTCUSDT')
            self.assertEqual(r_json['side'], order['side'])
            self.assertAlmostEqual(float(r_json['price']), order['price'], delta=0.01)
            self.assertAlmostEqual(float(r_json['origQty']), order['volume'], delta=0.001)


if __name__ == '__main__':
    unittest.main()
