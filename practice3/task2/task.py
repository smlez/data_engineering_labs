import re
import sys

sys.path.append('/home/jet/Documents/urfu-labs/data_engineering_labs/practice3')
from tasks_api import filter_items, get_markers, get_statistics, parse_files, parse_node, read_html, sort_items_by_key, write_to_file

def parse_fn(file_name: str):
    soup = read_html(file_name)
    data = {}
    data['id'] = parse_node(soup, 'a', "", {})['href'].split('/')[2]
    data['model'] = parse_node(soup, 'span', "", {}).strip()
    data['price'] = float(re.sub('\D', '', parse_node(soup, 'price', "", {})))
    data['bonuses'] = float(parse_node(soup, 'strong', "бонусов", {}).split('+ начислим')[1].split('бонусов')[0].strip())
    data['processor'] = parse_node(soup, 'li', "", {"type": "processor"}).strip()
    data['ram_gb'] = float(parse_node(soup, 'li', "", {"type": "ram"}).split("GB")[0].strip())
    data['sim'] = float(parse_node(soup, 'li', "", {"type": "sim"}).split("SIM")[0].strip())
    data['resolution'] = parse_node(soup, 'li', "", {"type": "resolution"}).strip()
    data['camera_mp'] = float(parse_node(soup, 'li', "", {"type": "camera"}).split("MP")[0].strip())

    return data

def compare_fn(item):
    return float(item['bonuses']) >= 1500.

items = parse_files(87, parse_fn)
write_to_file('parsed_items', items)
write_to_file('sorted_items', sort_items_by_key(items, 'camera_mp'))
write_to_file('filtered_items', filter_items(items, compare_fn))
write_to_file('result_stats', get_statistics(items, 'price'))
write_to_file('result_markers', get_markers(items, 'ram_gb'))