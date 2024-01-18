import pymongo
import json
from utils import get_object_list
from bson import json_util

def write_to_file(name: str, items: list):
    with open(name, 'w', encoding='utf-8') as f:
        f.write(json_util.dumps(items, ensure_ascii=False))

client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
db = client.test_database
collection = db.example_collection

collection.insert_many(get_object_list('task_1_item.msgpack'))

write_to_file('result_1', list(collection.find().sort("salary", -1).limit(10)))
write_to_file('result_2', list(collection.find({'age': {'$lt': 30}}).sort("salary", -1).limit(15)))
write_to_file('result_3', list(collection.find({"city": "Виго", "job": {"$in": ["Инженер", "Медсестра", "Водитель"]}}).sort("age", pymongo.ASCENDING).limit(10)))
write_to_file('result_4', collection.count_documents(
        {"age": {"$gte": 10, "$lte": 48},
         "year": {"$in": [2019, 2020, 2021, 2022]},
         "$or": [
             {"salary": {"$gt": 50000, "$lte": 75000}},
             {"salary": {"$gt": 125000, "$lt": 150000}}
         ]}
    ))