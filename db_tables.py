import psycopg2

conn = psycopg2.connect(
    database="postgres",
    user="myuser",
    password="mypassword",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

cur.execute("COMMIT")
cur.execute("DROP DATABASE IF EXISTS mydb")

cur.execute("CREATE DATABASE mydb WITH OWNER = myuser")

conn.commit()
cur.close()
conn.close()

conn = psycopg2.connect(
    database="mydb",
    user="myuser",
    password="mypassword",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255),
    contact_person VARCHAR(255),
    phone VARCHAR(20),
    billing_account VARCHAR(255)
)
""")

cur.execute("""
CREATE TABLE materials (
    material_id SERIAL PRIMARY KEY,
    material_name VARCHAR(255),
    price NUMERIC(10, 2)
)
""")

cur.execute("""
CREATE TABLE deliveries (
    delivery_id SERIAL PRIMARY KEY,
    delivery_date DATE,
    supplier_id INT,
    material_id INT,
    days_for_delivery INT CHECK (days_for_delivery >= 1 AND days_for_delivery <= 7),
    quantity_of_materials_delivered INT
)
""")

cur.execute("ALTER TABLE deliveries ADD CONSTRAINT fk_supplier FOREIGN KEY (supplier_id) REFERENCES suppliers (supplier_id);")
cur.execute("ALTER TABLE deliveries ADD CONSTRAINT fk_material FOREIGN KEY (material_id) REFERENCES materials (material_id);")

cur.execute("""
INSERT INTO suppliers (company_name, contact_person, phone, billing_account)
VALUES
    ('WoodCraft Suppliers', 'Contact1', '+1234567890', 'Account1'),
    ('Paints & Coatings Express', 'Contact2', '+2345678901', 'Account2'),
    ('Metal Works Producers', 'Contact3', '+3456789012', 'Account3'),
    ('EcoBuilding Materials', 'Contact4', '+4567890123', 'Account4');
""")

cur.execute("""
INSERT INTO materials (material_name, price)
VALUES
    ('Деревина', 10.00),
    ('Лак', 5.00),
    ('Сталеві деталі', 15.00);
""")

cur.execute("""
INSERT INTO deliveries (delivery_date, supplier_id, material_id, days_for_delivery, quantity_of_materials_delivered)
VALUES
    ('2023-11-08', 1, 1, 3, 100),
    ('2023-11-09', 2, 2, 5, 200),
    ('2023-11-10', 3, 3, 2, 150),
    ('2023-11-11', 4, 1, 7, 300),
    ('2023-11-12', 1, 3, 4, 250),
    ('2023-11-13', 2, 2, 6, 180),
    ('2023-11-14', 3, 1, 2, 120),
    ('2023-11-15', 4, 2, 1, 50),
    ('2023-11-16', 1, 1, 5, 320),
    ('2023-11-17', 2, 3, 3, 210),
    ('2023-11-18', 3, 2, 7, 280),
    ('2023-11-19', 4, 1, 2, 90),
    ('2023-11-20', 1, 3, 6, 180),
    ('2023-11-21', 2, 1, 4, 260),
    ('2023-11-22', 3, 2, 5, 150),
    ('2023-11-23', 4, 3, 3, 120),
    ('2023-11-24', 1, 2, 7, 220),
    ('2023-11-25', 2, 1, 2, 90),
    ('2023-11-26', 3, 3, 1, 50),
    ('2023-11-27', 4, 2, 5, 200),
    ('2023-11-28', 1, 1, 3, 160),
    ('2023-11-29', 2, 3, 6, 180);
""")

conn.commit()
cur.close()
conn.close()
