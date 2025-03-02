import sqlite3
import pandas as pd
from datetime import datetime

def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Customers table
    c.execute('''CREATE TABLE IF NOT EXISTS customers
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  phone TEXT NOT NULL,
                  workplace TEXT,
                  registration_date DATE)''')

    # Orders table
    c.execute('''CREATE TABLE IF NOT EXISTS orders
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  customer_id INTEGER,
                  square_meters REAL,
                  price_per_meter REAL,
                  banner_price REAL,
                  delivery_price REAL,
                  total_price REAL,
                  banner_dimensions TEXT,
                  delivery_status TEXT,
                  installation_status TEXT,
                  order_date DATE,
                  FOREIGN KEY (customer_id) REFERENCES customers (id))''')

    # Payments table
    c.execute('''CREATE TABLE IF NOT EXISTS payments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  order_id INTEGER,
                  amount REAL,
                  payment_date DATE,
                  FOREIGN KEY (order_id) REFERENCES orders (id))''')

    # Expenses table
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  description TEXT,
                  amount REAL,
                  expense_date DATE)''')

    conn.commit()
    conn.close()

def get_db():
    return sqlite3.connect('data.db')

def add_customer(name, phone, workplace):
    conn = get_db()
    c = conn.cursor()
    c.execute('''INSERT INTO customers (name, phone, workplace, registration_date)
                 VALUES (?, ?, ?, ?)''', (name, phone, workplace, datetime.now().date()))
    conn.commit()
    conn.close()

def get_customers():
    conn = get_db()
    df = pd.read_sql_query("SELECT * FROM customers", conn)
    conn.close()
    return df

def add_order(customer_id, square_meters, price_per_meter, banner_dimensions, 
              delivery_status, installation_status, banner_price=0, delivery_price=0):
    conn = get_db()
    c = conn.cursor()
    material_price = square_meters * price_per_meter
    total_price = material_price + banner_price + delivery_price

    c.execute('''INSERT INTO orders 
                 (customer_id, square_meters, price_per_meter, banner_price,
                  delivery_price, total_price, banner_dimensions,
                  delivery_status, installation_status, order_date)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (customer_id, square_meters, price_per_meter, banner_price,
               delivery_price, total_price, banner_dimensions,
               delivery_status, installation_status, datetime.now().date()))
    conn.commit()
    conn.close()

def get_orders():
    conn = get_db()
    df = pd.read_sql_query("""
        SELECT o.*, c.name as customer_name
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
    """, conn)
    conn.close()
    return df

def get_payments():
    conn = get_db()
    df = pd.read_sql_query("""
        SELECT p.*, o.total_price, c.name as customer_name
        FROM payments p
        JOIN orders o ON p.order_id = o.id
        JOIN customers c ON o.customer_id = c.id
    """, conn)
    conn.close()
    return df