import json
import msgpack
import os

with open("./products_72.json") as f:
    data = json.load(f)
    products = dict()

    for item in data: 
        if item['name'] in products:
            products[item['name']].append(item['price'])
        else:
            products[item['name']] = list()
            products[item['name']].append(item['price'])

    result = list()

    for name, prices in products.items():
        sum_p = 0
        max_p = prices[0]
        min_p = prices[0]
        size = len(prices)
        for price in prices:
            sum_p += price
            max_p = max(max_p, price)
            min_p = min(min_p, price)

        result.append({
            "name": name,
            "max": max_p,
            "min": min_p,
            "avr": sum_p / size
        })

        with open("products_result.json", "w") as r_json:
            r_json.write(json.dumps(result))

        with open("products_result.msgpack", "wb") as r_msgpack:
            r_msgpack.write(msgpack.dumps(result))

json_file = os.path.getsize('products_result.json')
msgpack_file = os.path.getsize('products_result.msgpack')

if (json_file < msgpack_file):
    print(f"JSON файл весит меньше файла формата msgpack на {msgpack_file - json_file}")
else:
    print(f"msgpack файл весит меньше файла формата json на {json_file - msgpack_file}")