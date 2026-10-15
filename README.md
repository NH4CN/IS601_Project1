# My Python Project
Dosa Restaurant Midterm Project

## Project Overview

This Python project is designed to help a Dosa restaurant organize its order information. The program reads customer orders from a JSON file and processes the data into a more organized format.

The goal is to create separate JSON files containing customer information and menu item statistics.


## Current Features
- Load Orders: Reads order information from a JSON file provided as a command-line argument.
- Customer Information: Extracts customer names and phone numbers from the orders.
- Duplicate Prevention: Uses a dictionary to ensure each phone number appears only once.
- Menu Item Tracking: Extracts customer names and prices while counting how many times each item has been ordered.
- JSON File Creation: Saves processed information into separate JSON files using formatted output.

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

### 4. create_items(orders)

This function processes the menu items from each customer order and creates a dictionary containing item information.
- Iterates through each order and its list of purchased items.
- Extracts each item's name and price.
- Creates a dictionary entry for each unique menu item.
- Initializes the order count to zero for new items.
- Increments the order count every time an item appears in an order.

### 5. save_json(filename, data)

This function saves processed Python dictionaries into JSON files.
- Opens or creates a file using write mode ('w').
- Uses json.dump() to convert Python data into JSON format.
- Uses indent=4 to make the output easier to read.
- Automatically closes the file using a with statement.

The function will be used to generate:
- customers.json: Stores customer phone numbers and names.
- items.json: Stores menu item prices and total order counts.

### 6. main()

The main function connects all the previously defined functions and executes the program.
- Checks that exactly once command-line argument has been provided.
- Displays a usage message and exits if the filename is missing or extra arguments are supplied.
- Loads customer orders from the specified JSON file.
- Creates dictionaries containing customer information and menu item statistics.
- Saves the processed information into customers.json and items.json.


## Technologies Used
- Python 3
- JSON
- Git and GitHub
- Visual Studio Code

## Author
Neelansh Keshari