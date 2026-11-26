import os
import mysql.connector
from dotenv import load_dotenv
import random
import time
from datetime import date, timedelta


load_dotenv()

mydb = None
mycursor = None
first_names = ["Ahmad", "Mohammad", "Omar", "Ali", "Khaled", "Yousef", "Hamza", "Ibrahim", "Adam", "Zaid", "Sara", "Layan", "Noor", "Hala", "Reem", "Aya", "Farah", "Lina", "Dana", "Mariam"]
last_names = ["Al-Hassan", "Al-Ahmad", "Al-Khatib", "Al-Jallad", "Al-Masri", "Al-Najjar", "Al-Haddad", "Al-Salem", "Al-Khalil", "Al-Omar", "Al-Tamimi", "Al-Abbadi", "Al-Zoubi", "Al-Smadi", "Al-Majali", "Al-Rashdan", "Al-Kurdi", "Al-Shami", "Al-Nasser", "Al-Hamdan"]
cities = ["Amman", "Zarqa", "Irbid", "Aqaba", "Madaba", "Jerash", "Ajloun", "Karak", "Salt", "Mafraq", "Tafilah", "Maan", "Dubai", "Riyadh", "Cairo", "Doha", "Beirut", "Baghdad", "Muscat", "Kuwait City"]
phone = ['079', '078', '077']
product = {
    "Electronics": ["Smartphone", "Smartwatch", "Camera"],
    "Computers": ["Laptop", "Monitor", "Tablet"],
    "Accessories": ["Keyboard", "Mouse", "Headphones"],
    "Furniture": ["Office Chair", "Desk", "Bookshelf"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket"],
    "Footwear": ["Running Shoes", "Sandals", "Boots"],
    "Home Appliances": ["Refrigerator", "Washing Machine", "Microwave"],
    "Kitchenware": ["Coffee Maker", "Blender", "Frying Pan"],
    "Sports": ["Football", "Dumbbells", "Tennis Racket"],
    "Beauty": ["Perfume", "Shampoo", "Face Cream"],
    "Health": ["Thermometer", "Blood Pressure Monitor", "First Aid Kit"],
    "Books": ["Programming Book", "History Book", "Novel"],
    "Toys": ["Teddy Bear", "Puzzle", "Toy Car"],
    "Gaming": ["Gaming Console", "Controller", "Gaming Headset"],
    "Automotive": ["Car Battery", "Engine Oil", "Car Charger"],
    "Groceries": ["Rice", "Pasta", "Olive Oil"],
    "Office Supplies": ["Printer", "Stapler", "Paper Shredder"],
    "Tools": ["Hammer", "Screwdriver", "Electric Drill"],
    "Jewelry": ["Ring", "Necklace", "Bracelet"],
    "Stationery": ["Notebook", "Pencil", "Pen"]
}
categories = ["Electronics", "Computers", "Accessories", "Furniture", "Clothing", "Footwear", "Home Appliances", "Kitchenware", "Sports", "Beauty", "Health", "Books", "Toys", "Gaming", "Automotive", "Groceries", "Office Supplies", "Tools", "Jewelry", "Stationery"]
status = ['Pending','Completed','Cancelled']


def generate_radom_date():
    start_date = date(2023, 1, 1)
    end_date = date.today()

    random_date = start_date + timedelta(
        days=random.randint(0, (end_date - start_date).days)
    )

    return random_date

def fetch_customer():
    sql = "SELECT id FROM customers"
    mycursor.execute(sql)
    customses = mycursor.fetchall()
    return [row[0] for row in customses]

def fetch_order():
    sql = 'SELECT id FROM orders'
    mycursor.execute(sql)
    orders = mycursor.fetchall()
    return [row[0] for row in orders]

def fetch_product():
    products = None
    sql = "SELECT id, price FROM products"
    mycursor.execute(sql)
    products = tuple((key, float(values)) for key, values in mycursor.fetchall())
    return [row for row in products]





def geterate_customer():
    customers = []
    sql = "INSERT INTO customers (first_name, last_name, email, phone, city) VALUES (%s, %s, %s, %s, %s)"

    for i in range(10000):
        first_name_random = random.choice(first_names)
        last_names_random = random.choice(last_names)
        email = f"{first_name_random}.{last_names_random}{i}@example.com"
        number = random.randint(1000000, 9999999)
        random_number = f"{random.choice(phone)}{number}"
        city = random.choice(cities)
        val = (first_name_random, last_names_random, email, random_number, city )
        customers.append(val)

    mycursor.executemany(sql, customers)

def generate_products():
    products = []
    sql= "INSERT INTO products (name, category, price, stock_quantity) VALUES (%s, %s, %s, %s)"
    for i in range(0, 1000):
        category = random.choice(categories)
        name = random.choice(product[category])
        price = round(random.uniform(0.50, 5000.00), 2)
        stock = random.randint(0, 1000)
        val = (name, category, price, stock)
        products.append(val)
    mycursor.executemany(sql, products)
    print("Products inserted successfuly")

def generate_order_items():
    order_item = []
    sql = "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, %s, %s, %s)"
    orders = fetch_order()
    pruducts = fetch_product()
    if not pruducts or not orders :
        raise Exception('Product or orders are empty')
    
    
    for order in orders:
        product = random.choice(pruducts)
        product_id = product[0]
        product_price = product[1]
        quity = random.randint(1 , 10)
        vals = (order, product_id, quity, product_price)
        order_item.append(vals)

    for i in range(100000):
        order_id = random.choice(orders)
        product = random.choice(pruducts)
        product_id = product[0]
        product_price = product[1]
        quity = random.randint(1 , 10)
        vals = (order_id, product_id, quity, product_price)
        order_item.append(vals)

    mycursor.executemany(sql, order_item)
 
def generate_orders():
    orders = []
    sql = 'INSERT INTO orders (customer_id, order_date, status, total_amount) VALUES (%s, %s, %s, %s)'
    customers_id = fetch_customer()
    if len(customers_id) > 0:
        for i in range(100000):
            rand_date = generate_radom_date()
            order_status = random.choice(status)
            total_amount = 0
            val = (random.choice(customers_id), rand_date, order_status, total_amount)
            orders.append(val)
        mycursor.executemany(sql, orders)
        print("order inserted successfuly")
    else:
        raise Exception ("Customer table is empty")

def updated_orders_items():
    sql = """UPDATE orders 
             JOIN(
                SELECT order_id, SUM(quantity * unit_price) AS total_price FROM order_items 
                GROUP BY order_id 
                ) AS order_item
            ON orders.id = order_item.order_id
            SET total_amount = order_item.total_price"""
    mycursor.execute(sql)            




try:
    mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    username=os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
    )

    mycursor = mydb.cursor()

    if mycursor is not None:
        try:
            
            start_time = time.perf_counter()

            # generate_products()
            # generate_orders()
            # generate_order_items()
            updated_orders_items()

            mydb.commit()
            end_time = time.perf_counter()
            duration = end_time - start_time
            print(f"rows inserted successfuly")
            print (f"{mycursor.rowcount} has been inserted")
            print(f"time it take to excute {duration}")

        except Exception as e:
            mydb.rollback()
            print(f"Error:{e}")

        
    else:
        print("connection lost")
except mysql.connector.Error as e:
    print(f"Error: {e}")
finally:
    if mycursor is not None:
        mycursor.close()

    if mydb is not None:
        mydb.close()


