import pickle
import pymongo
from bson import json_util


client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
db = client.test_database
collection = db.example_collection

def load_pickle():
    with open('task_3_item.pkl', "rb") as file:
        data_file = pickle.load(file)
    return data_file

def write_file(data, fileName):
    with open('./'+fileName+'.json', 'w', encoding='utf-8') as out:
        out.write(json_util.dumps(data, ensure_ascii=False))

collection.insert_many(load_pickle())

selected_jobs = ["Медсестра", "Учитель"]
selected_cities = ["Куэнка", "Сория"]

collection.delete_many({"$or": [{"salary": {"$lt": 25000}}, {"salary": {"$gt": 175000}}]})
write_file(list(collection.find()), 'results/1')
collection.update_many({}, {"$inc": {"age": 1}})
write_file(list(collection.find()), 'results/2')
collection.update_many({"job": {"$in": selected_jobs}}, {"$mul": {"salary": 1.05}})
write_file(list(collection.find()), 'results/3')
collection.update_many({"city": {"$in": selected_cities}}, {"$mul": {"salary": 1.07}})
write_file(list(collection.find()), 'results/4')

selected_predicate = {"city": "Тбилиси", "job": {"$in": ["Менеджер", "Программист"]}, "age": {"$gte": 30, "$lte": 50}}
collection.update_many(selected_predicate, {"$mul": {"salary": 1.1}})
write_file(list(collection.find()), 'results/5')

delete_predicate = {"year": {"$lt": 2001}}
collection.delete_many(delete_predicate)

write_file(list(collection.find()), 'results/6')