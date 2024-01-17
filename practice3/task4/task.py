import re
import sys

sys.path.append('/home/jet/Documents/urfu-labs/data_engineering_labs/practice3')
from tasks_api import filter_items, get_markers, get_statistics, parse_files, parse_node, read_xml, sort_items_by_key, write_to_file

def parse_fn(file_name: str):
    soup = read_xml(file_name)
    data = {}
    data['id'] = int(parse_node(soup, 'id', "", {}).strip())
    data['name'] = parse_node(soup, 'name', "", {}).strip()
    data['category'] = parse_node(soup, 'category', "", {}).strip()
    data['size'] = parse_node(soup, 'size', "", {}).strip()
    data['color'] = parse_node(soup, 'color', "", {}).strip()
    data['material'] = parse_node(soup, 'material', "", {}).strip()
    data['price'] = float(parse_node(soup, 'price', "", {}).strip())
    data['rating'] = float(parse_node(soup, 'rating', "", {}).strip())
    data['reviews'] = int(parse_node(soup, 'reviews', "", {}).strip())
    data['new'] = parse_node(soup, 'new', "", {}).strip()
    data['sporty'] = parse_node(soup, 'sporty', "", {}).strip()

    data['new'] = True if data['new'] == "+" else False
    data['sporty'] = True if data['sporty'] == "yes" else False

    return data

def compare_fn(item):
    return item['new']

items = parse_files(100, parse_fn, 'xml')
write_to_file('parsed_items', items)
write_to_file('sorted_items', sort_items_by_key(items, 'rating'))
write_to_file('filtered_items', filter_items(items, compare_fn))
write_to_file('result_stats', get_statistics(items, 'price'))
write_to_file('result_markers', get_markers(items, 'category'))