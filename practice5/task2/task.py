import pymongo

from utils import get_object_list
from bson import json_util

client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
db = client.test_database
collection = db.example_collection

collection.insert_many(get_object_list('task_2_item.json'))

def write_file(data, fileName):
    with open('./'+fileName+'.json', 'w', encoding='utf-8') as out:
        out.write(json_util.dumps(data, ensure_ascii=False))

# 1 вывод минимальной, средней, максимальной salary 
# 2 вывод количества данных по представленным профессиям 
# 3 вывод минимальной, средней, максимальной salary по городу 
# 4 вывод минимальной, средней, максимальной salary по профессии 
# 5 вывод минимального, среднего, максимального возраста по городу 
# 6 вывод минимального, среднего, максимального возраста по профессии  
# 7 вывод максимальной заработной платы при минимальном возрасте 
# 8 вывод минимальной заработной платы при максимальной возрасте 
# 9 вывод минимального, среднего, максимального возраста по городу, при условии, что заработная плата больше 50 000, отсортировать вывод по любому полю. 
# 10 вывод минимальной, средней, максимальной salary в произвольно заданных диапазонах по городу, профессии, и возрасту: 18<age<25 & 50<age<65 
# 11 произвольный запрос с $match, $group, $sort 

write_file(list(collection.aggregate([
        {"$group": {"_id": None, "min_salary": {"$min": "$salary"}, "avg_salary": {"$avg": "$salary"}, "max_salary": {"$max": "$salary"}}}
    ])), 'results/1)')
write_file(list(collection.aggregate([
        {"$group": {"_id": "$job", "count": {"$sum": 1}}}
    ])), 'results/2)')
write_file(list(collection.aggregate([
        {"$group": {"_id": "$city", "min_salary": {"$min": "$salary"}, "avg_salary": {"$avg": "$salary"}, "max_salary": {"$max": "$salary"}}}
    ])), 'results/3)')
write_file(list(collection.aggregate([
        {"$group": {"_id": "$job", "min_salary": {"$min": "$salary"}, "avg_salary": {"$avg": "$salary"}, "max_salary": {"$max": "$salary"}}}
    ])), 'results/4)')
write_file(list(collection.aggregate([
        {"$group": {"_id": "$city", "min_age": {"$min": "$age"}, "avg_age": {"$avg": "$age"}, "max_age": {"$max": "$age"}}}
    ])), 'results/5)')
write_file(list(collection.aggregate([
        {"$group": {"_id": "$job", "min_age": {"$min": "$age"}, "avg_age": {"$avg": "$age"}, "max_age": {"$max": "$age"}}}
    ])), 'results/6)')
write_file(list(collection.aggregate([
        {"$group": {"_id": "$age", "max_salary": {"$max": "$salary"}}},
        {"$sort": {"_id": 1}},
        {"$limit": 1}
    ])), 'results/7)')
write_file(list(collection.aggregate([
        {"$group": {"_id": "$age", "min_salary": {"$min": "$salary"}}},
        {"$sort": {"_id": -1}},
        {"$limit": 1}
    ])), 'results/8)')
write_file(list(collection.aggregate([
        {"$match": {"salary": {"$gt": 50000}}},
        {"$group": {"_id": "$city", "min_age": {"$min": "$age"}, "avg_age": {"$avg": "$age"}, "max_age": {"$max": "$age"}}},
        {"$sort": {"_id": 1}}
    ])), 'results/9)')
write_file(list(collection.aggregate([
        {"$match": {"age": {"$in": list(range(18, 25)) + list(range(50, 65))}}},
        {"$group": {"_id": {"city": "$city", "job": "$job"}, "min_salary": {"$min": "$salary"}, "avg_salary": {"$avg": "$salary"}, "max_salary": {"$max": "$salary"}}}
    ])), 'results/10')
write_file(list(collection.aggregate([
        {"$match": {"city": "Астана", "job": "Строитель"}},
        {"$group": {"_id": "$year", "avg_salary": {"$avg": "$salary"}}},
        {"$sort": {"avg_salary": -1}}
    ])), 'results/11')