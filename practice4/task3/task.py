import os
import sqlite3
import json
import pickle

f_1 = os.path.join(os.path.dirname(__file__), os.path.normpath('task_3_var_72_part_2.text'))
f_2 = os.path.join(os.path.dirname(__file__), os.path.normpath('task_3_var_72_part_1.json'))

def read_file_1():
    data=[]
    with open(f_1,encoding='utf-8') as file:
        lines = file.readlines()
        item={}
        for line in lines:
            value=str(line).split(':')
            if line == "=====\n":
                data.append(item)
                item={}
                continue
            cleared_value=value[2].replace('\n','')
            if value[0] in('instrumentalness', 'loudness'):
                continue
            if value[0] in('artist','song', 'genre'):
                item[value[0]]=str(cleared_value)
            elif value[0] in ('tempo'):
                item[value[0]]=float(cleared_value)
            elif value[0] in ('explicit'):
                item[value[0]]=bool(cleared_value)
            else:
                item[value[0]]=int(cleared_value)
                
    return data

def read_file():
    with open(f_2, 'r', encoding='utf-8') as file:
        data=json.loads(file.read())
        for item in data:
            item.pop('popularity')
            item.pop('danceability')
        return data


def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection

def create_table(db):
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS music(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   artist TEXT,
   song TEXT,
   duration_ms INTEGER,
   year INTEGER,
   tempo REAL,
   genre TEXT,
   explicit BOOLEAN);
""")
    db.commit()

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO music
            (artist, song, duration_ms, year, tempo, genre, explicit) 
        VALUES
            (:artist, :song, :duration_ms, :year, :tempo, :genre, :explicit)""", data)
    db.commit()


def top_duration_ms(db, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM music ORDER BY duration_ms DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


def charact_tempo(db):
    cursor = db.cursor()
    items = []
    res = cursor.execute("""
        SELECT 
            SUM(tempo) as sum,
            AVG(tempo) as avg,
            MIN(tempo) as min, 
            MAX(tempo) as max
        FROM music
                        """)
    # print(dict(res.fetchone()))
    # cursor.close()
    for row in res.fetchall():
        items.append(dict(row))
        print(dict(row))
    return items


def popul_genre(db):
    cursor = db.cursor()
    items = []
    res = cursor.execute("""
        SELECT 
            CAST(COUNT(*) as REAL) / (SELECT COUNT(*) FROM music) as count,
            genre
        FROM music
        GROUP BY genre
                        """)
    for row in res.fetchall():
        items.append(dict(row))
        print(dict(row))
    return items


def filter_year(db, min_pop, limit):
    items = []
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM music
        WHERE year >= ?
        ORDER BY year DESC
        LIMIT ?
        """, [min_pop, limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items

db = connect_to_db('db')
create_table(db)
d_1 = read_file_1()
d_2 = read_file()
insert_data(db, d_1)
insert_data(db, d_2)

with open('1', 'w', encoding='utf-8') as f:
    f.write(json.dumps(top_duration_ms(db, 70+10), ensure_ascii=False))

with open('2', 'w', encoding='utf-8') as f:
    f.write(json.dumps(charact_tempo(db), ensure_ascii=False))

with open('3', 'w', encoding='utf-8') as f:
    f.write(json.dumps(popul_genre(db), ensure_ascii=False))

with open('4', 'w', encoding='utf-8') as f:
    f.write(json.dumps(filter_year(db, 1995, 70+15), ensure_ascii=False))