import re
import sys

sys.path.append('/home/jet/Documents/urfu-labs/data_engineering_labs/practice3')
from tasks_api import filter_items, get_markers, get_statistics, parse_files, parse_node, read_xml, sort_items_by_key, write_to_file

def parse_fn(file_name: str):
    soup = read_xml(file_name)
    data = {}
    data['name'] = parse_node(soup, 'name', "", {}).strip()
    data['constellation'] = parse_node(soup, 'constellation', "", {}).strip()
    data['spectral-class'] = parse_node(soup, 'spectral-class', "", {}).strip()
    data['radius'] = float(parse_node(soup, 'radius', "", {}).strip())
    data['days-to-rotate'] = float(parse_node(soup, 'rotation', "", {}).split('days')[0].strip())
    data['age-billion-years'] = float(parse_node(soup, 'age', "", {}).strip().split(' ')[0])
    data['distance'] = float(parse_node(soup, 'distance', "", {}).strip().split(' ')[0])
    data['magnitude'] = float(parse_node(soup, 'absolute-magnitude', "", {}).strip().split(' ')[0])

    return data

def compare_fn(item):
    return float(item['days-to-rotate']) >= 700.

items = parse_files(500, parse_fn, 'xml')
write_to_file('parsed_items', items)
write_to_file('sorted_items', sort_items_by_key(items, 'age-billion-years'))
write_to_file('filtered_items', filter_items(items, compare_fn))
write_to_file('result_stats', get_statistics(items, 'magnitude'))
write_to_file('result_markers', get_markers(items, 'spectral-class'))