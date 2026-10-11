# My Python Project
Dosa Restaurant Midterm Project

## Project Overview

This Python project is designed to help a Dosa restaurant organize its order information. The program reads customer orders from a JSON file and processes the data into a more organized format.

The goal is to create separate JSON files containing customer information and menu item statistics.


## Current Features
- Load Orders: Reads order information from a JSON file provided as a command-line argument.
- Customer Information: Extracts customer names and phone numbers from the orders.
- Duplicate Prevention: Uses a dictionary to ensure each phone number appears only once.


## Program Design

### 1. Import Libraries

The program uses two built-in Python libraries:

- json: Reads and processes JSON data.
- sys: Allows the program to accept a filename through command-line arguements.

### 2. load_orders(filename)

This function opens the specified JSON file and loads its contents into Python using json.load().

### 3. create_customers(orders)

This function processes the orders and creates a dictionary containing customer information.
- Iterates through each order.
- Extracts the customer's phone number and name.
- Uses the phone number as the dictionary key and the customer's name as the value.
- Prevents duplicate phone number entries because dictionary keys must be unique.

### Example Customer Data:

{
	"732-555-5509": "Damodhar",
	"609-555-2301": "Tom"
}


## Input File

The program uses example_orders.json, which contains customer orders, including timestamps, customer names, phone numbers, purchased items, prices, and notes.


## Planned Features
- Create an items.json file containing menu item prices and order counts.
- Save the processed customer information into customers.json
- Implement the main function to process command-line arguments and execute the program.


## Technologies Used
- Python 3
- JSON
- Git and GitHub
- Visual Studio Code

## Author
Neelansh Keshari