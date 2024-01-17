
import json
import re
import statistics
from bs4 import BeautifulSoup

def read_html(file_name: str) -> BeautifulSoup:
    with open(file_name, encoding='utf-8') as f:
        html = ''
        lines = f.readlines()
        for line in lines:
            html += line
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    
def read_xml(file_name: str) -> BeautifulSoup:
    with open(file_name, encoding='utf-8') as f:
        xml = ''
        lines = f.readlines()
        for line in lines:
            xml += line
        soup = BeautifulSoup(xml, 'xml')
        return soup

def parse_files(count: int, parse_fn, ext: str = 'html'):
    items = []
    for i in range(1, count + 1):
        try:
            value = parse_fn(f"zip_var_72/{i}.{ext}")
            items.append(value)
        except Exception as e:
            print(e, i)

    return items

def parse_node(soup: BeautifulSoup, tag: str, compile: str, attrs: dict):
    node = ""
    if tag == "img":
        node = soup.find_all('img')[0]['src']
    elif tag == "a":
        node = soup.find_all('a', href=True)[1]
    else:
        node = re.sub(r'\n', '', soup.find_all(tag, string=re.compile(compile), attrs=attrs)[0].get_text())

    
    return node
    

def sort_items_by_key(list: list, key: str, reverse: bool = True):
    return sorted(list, key=lambda x: x[key], reverse=reverse)

def filter_items(items: list, filter_fn):
    filtered_items = []
    for item in items:
        if filter_fn(item):
            filtered_items.append(item)
    return filtered_items

def write_to_file(name: str, items: list):
    with open(name, 'w', encoding='utf-8') as f:
        f.write(json.dumps(items, ensure_ascii=False))

def get_statistics(items: list, param: str):
    data = {}
    data['sum'] = 0
    data['min'] = float('inf')
    data['max'] = float('-inf')
    std = [0]
    for item in items:
        value = float(item[param])
        data['sum'] += value
        if data['min'] > value:
            data['min'] = value
        if data['max'] < value:
            data['max'] = value
        std.append(value)
    data['avr'] = data['sum'] / len(items)
    data['std'] = statistics.stdev(std)

    return data

def get_markers(items: list, param: str):
    data = {}
    for item in items:
        if item[param] in data:
            data[item[param]] += 1
        else:
            data[item[param]] = 1

    return data