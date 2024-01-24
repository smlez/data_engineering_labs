import os
import sqlite3
import json
import sys

sys.path.append('/home/jet/Documents/urfu-labs/data_engineering_labs/practice4')
from utils import get_object_list

def read_file():
    data=[]
    with open('task_1_var_72_item.text',encoding='utf-8') as file:
        lines = file.readlines()
        item={}
        for line in lines:
            value=str(line).split(':')
            if line == "=====\n":
                data.append(item)
                item={}
                continue
            cleared_value=value[2].replace('\n','')
            if value[0] in('title','author','genre', 'isbn'):
                item[value[0]]=str(cleared_value)
            elif value[0] in ('rating'):
                item[value[0]]=float(cleared_value)
            else:
                item[value[0]]=int(cleared_value)
                
    return data

def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection

def create_table(db):
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS books")
    cursor.execute("""
        CREATE TABLE books(
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            genre TEXT(20),
            pages INTEGER,
            published_year INTEGER,
            isbn TEXT,
            rating FLOAT,
            views INTEGER
        );
""")
    db.commit()

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO books 
        (title, author, genre, pages, published_year, isbn, rating, views) 
        VALUES
        (:title, :author, :genre, :pages, :published_year, :isbn, :rating, :views)""", data)
    db.commit()



def sort_by_years(db, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM books ORDER BY published_year DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


def charact_views(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            SUM(views) as sum,
            AVG(views) as avg,
            MIN(views) as min, 
            MAX(views) as max
        FROM books
                        """)
    print(dict(res.fetchone()))
    cursor.close()
    return None


def genre_stats(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            CAST(COUNT(*) as REAL) / (SELECT COUNT(*) FROM books) as count,
            genre
        FROM books
        GROUP BY genre
                        """)
    for row in res.fetchall():
        print(dict(row))
    return None


def filter_by_pages(db, min, limit):
    items = []
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM books
        WHERE pages >= ?
        ORDER BY pages DESC
        LIMIT ?
        """, [min, limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items



db = connect_to_db('db')
create_table(db)
data = read_file()
insert_data(db, data)


charact_views(db)
genre_stats(db)

with open('sort_views', 'w', encoding='utf-8') as f:
    f.write(json.dumps(sort_by_years(db, 72+10), ensure_ascii=False))

with open('filter_by_pages', 'w', encoding='utf-8') as f:
    f.write(json.dumps(filter_by_pages(db, 200, 72+10), ensure_ascii=False))