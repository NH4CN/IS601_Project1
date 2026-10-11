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