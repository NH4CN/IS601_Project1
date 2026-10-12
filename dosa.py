import json
import sys

def load_orders(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def create_customers(orders):
    customers = {}
    for order in orders:
        phone = order['phone']
        name = order['name']
        customers[phone] = name
    return customers

def create_items(orders):
    items = {}
    for order in orders:
        for item in order['items']:
            item_name = item['name']
            item_price = item['price']
            if item_name not in items:
                item[item_name] = {
                    'price': item_price,
                    'orders': 0
                }
            items[item_name]['orders'] += 1
    return items

def save_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)