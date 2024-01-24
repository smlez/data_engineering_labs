import os
import sqlite3
import json
import sys

def read_file_1():
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

def read_file():
    with open('task_2_var_72_subitem.json',encoding='utf-8') as file:
        json_string=file.read()
        return json.loads(json_string)

def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection

def create_table(db):
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS books2")
    cursor.execute("""
        CREATE TABLE books2(
            id INTEGER PRIMARY KEY,
            title TEXT,
            price INTEGER,
            place TEXT(20),
            date TEXT
        );
    """)
    db.commit()

def create_table_1(db):
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

def insert_data_1(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO books 
        (title, author, genre, pages, published_year, isbn, rating, views) 
        VALUES
        (:title, :author, :genre, :pages, :published_year, :isbn, :rating, :views)""", data)
    db.commit()

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO books2
        (title, price, place, date) 
        VALUES
        (:title, :price, :place, :date)""", data)
    db.commit()

def filter_1(db, min):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT * 
        FROM books
        WHERE (SELECT AVG(price) FROM books2 WHERE books2.title==books.title) > ?                
         """, [min])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    print(items)
    return None  


def filter_2(db,name):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            SUM(price) as sum,
            AVG(price) as avg,
            MIN(price) as min, 
            MAX(price) as max
        FROM books2
        WHERE title = (SELECT title FROM books WHERE title= ?)                
         """, [name])
    print(dict(res.fetchone()))
    cursor.close()
    return None


def filter_3(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            price
        FROM books2
        JOIN books ON books2.title = books.title
    """)
    for row in res.fetchall():
        print(dict(row))
    return None

db = connect_to_db('db')
create_table_1(db)
create_table(db)
data_1 = read_file_1()
data = read_file()
insert_data_1(db, data_1)
insert_data(db, data)

filter_1(db, 1)
# filter_2(db, '1984')
# filter_3(db)