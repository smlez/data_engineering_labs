import requests
import json
from json2html import *

API_URL="https://dummyjson.com/todos"

res = requests.get(API_URL)
jsonData = json.loads(res.text)
# print(json2html.convert(json = jsonData))

with open("result.html", "w") as res:
    res.write(json2html.convert(json = jsonData))
