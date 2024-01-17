import sys

sys.path.append('/home/jet/Documents/urfu-labs/data_engineering_labs/practice3')
from tasks_api import filter_items, get_markers, get_statistics, parse_files, parse_node, read_html, sort_items_by_key, write_to_file

def parse_fn(file_name: str):
    soup = read_html(file_name)
    data = {}
    data['type'] = parse_node(soup, 'span', "Тип", {}).split(':')[1].strip()
    data['tournment'] = parse_node(soup, 'h1', "", {}).split('Турнир:')[1].strip()
    data['city'] = parse_node(soup, 'p', "", {'class': 'address-p'}).split(': ')[1].split('Начало')[0].strip()
    data['start_date'] = parse_node(soup, 'p', "", {'class': 'address-p'}).split(':')[2].strip()
    data['tours_count'] = parse_node(soup, 'span', "", {'class': 'count'}).split(':')[1].strip()
    data['time_control_min'] = parse_node(soup, 'span', "", {'class': 'year'}).split(':')[1].split('мин')[0].strip()
    data['min_rating'] = parse_node(soup, 'span', "Минимальный рейтинг для участия", {}).split(':')[1].strip()
    data['img_url'] = parse_node(soup, 'img', "", {})
    data['rating'] = parse_node(soup, 'span', "Рейтинг", {}).split(':')[1].strip()
    data['views'] = parse_node(soup, 'span', "Просмотры", {}).split(':')[1].strip()

    return data

def compare_fn(item):
    return float(item['rating']) >= 3

items = parse_files(1000, parse_fn)
write_to_file('parsed_items', items)
write_to_file('sorted_items', sort_items_by_key(items, 'views'))
write_to_file('filtered_items', filter_items(items, compare_fn))
write_to_file('result_stats', get_statistics(items, 'rating'))
write_to_file('result_markers', get_markers(items, 'city'))