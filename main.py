import psycopg2

conn = psycopg2.connect(
    database="mydb",
    user="myuser",
    password="mypassword",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Відобразити всі поставки, які здійснюються за 3 або менше днів та відсортовані за назвами постачальників
cur.execute("""
SELECT s.company_name, to_char(d.delivery_date, 'YYYY-MM-DD'), m.material_name, d.days_for_delivery
FROM suppliers s
JOIN deliveries d ON s.supplier_id = d.supplier_id
JOIN materials m ON m.material_id = d.material_id
WHERE d.days_for_delivery <= 3
ORDER BY s.company_name;
""")
rows = cur.fetchall()

if rows:
    print("\nВсі поставки, які здійснюються за 3 або менше днів та відсортовані за назвами постачальників:")
    column_names = ["Назва компанії", "Дата поставки", "Назва матеріалу", "Днів для поставки"]
    column_widths = [25, 15, 15, 15]
    for i in range(len(column_names)):
        print("{:<{width}}".format(column_names[i], width=column_widths[i]), end=" ")
    print("\n" + "-" * sum(column_widths))

    for row in rows:
        for i in range(len(row)):
            print("{:<{width}}".format(row[i], width=column_widths[i]), end=" ")
        print()
else:
    print("Немає результатів для цього запиту.")

# Порахувати суму, яку треба сплатити за кожну поставку
cur.execute("""
SELECT d.delivery_id, s.company_name, m.material_name, d.quantity_of_materials_delivered * m.price AS total_price
FROM deliveries d
JOIN suppliers s ON s.supplier_id = d.supplier_id
JOIN materials m ON m.material_id = d.material_id;
""")
rows = cur.fetchall()

if rows:
    print("\nСума для кожної поставки:")
    column_names = ["Код поставки", "Назва компанії", "Назва матеріалу", "Сума для сплати"]
    column_widths = [15, 25, 15, 15]
    for i in range(len(column_names)):
        print("{:<{width}}".format(column_names[i], width=column_widths[i]), end=" ")
    print("\n" + "-" * sum(column_widths))

    for row in rows:
        for i in range(len(row)):
            print("{:<{width}}".format(row[i], width=column_widths[i]), end=" ")
        print()
else:
    print("Немає результатів для цього запиту.")

# Відобразити всі поставки обраного матеріалу
material_name = "Деревина"
cur.execute("""
SELECT d.delivery_id, s.company_name, to_char(d.delivery_date, 'YYYY-MM-DD'), d.quantity_of_materials_delivered, d.days_for_delivery
FROM suppliers s
JOIN deliveries d ON s.supplier_id = d.supplier_id
JOIN materials m ON m.material_id = d.material_id
WHERE m.material_name = %s;
""", (material_name,))
rows = cur.fetchall()

if rows:
    print(f"\nВсі поставки матеріалу '{material_name}':")
    column_names = ["Код поставки", "Назва компанії", "Дата поставки", "кількість матеріалів", "Днів для поставки"]
    column_widths = [15, 25, 15, 20, 15]
    for i in range(len(column_names)):
        print("{:<{width}}".format(column_names[i], width=column_widths[i]), end=" ")
    print("\n" + "-" * sum(column_widths))

    for row in rows:
        for i in range(len(row)):
            print("{:<{width}}".format(row[i], width=column_widths[i]), end=" ")
        print()
else:
    print(f"Немає результатів для цього запиту для матеріалу '{material_name}'.")

# Порахувати кількість кожного матеріалу, що поставляється кожним постачальником
cur.execute("""
SELECT s.company_name, m.material_name, SUM(d.quantity_of_materials_delivered) AS total_quantity
FROM suppliers s
JOIN deliveries d ON s.supplier_id = d.supplier_id
JOIN materials m ON m.material_id = d.material_id
GROUP BY s.company_name, m.material_name;
""")
rows = cur.fetchall()

if rows:
    print("\nКількість кожного матеріалу, що поставляється кожним постачальником:")
    column_names = ["Назва постачальника", "Назва матеріалу", "Кількість матеріалу"]
    column_widths = [25, 15, 15]
    for i in range(len(column_names)):
        print("{:<{width}}".format(column_names[i], width=column_widths[i]), end=" ")
    print("\n" + "-" * sum(column_widths))

    for row in rows:
        for i in range(len(row)):
            print("{:<{width}}".format(row[i], width=column_widths[i]), end=" ")
        print()
else:
    print("Немає результатів для цього запиту.")

# Порахувати загальну кількість кожного матеріалу
cur.execute("""
SELECT m.material_name, SUM(d.quantity_of_materials_delivered) AS total_quantity
FROM materials m
JOIN deliveries d ON m.material_id = d.material_id
GROUP BY m.material_name;
""")
rows = cur.fetchall()

if rows:
    print("\nЗагальна кількість кожного матеріалу:")
    column_names = ["Назва матеріалу", "Загальна кількість"]
    column_widths = [15, 15]
    for i in range(len(column_names)):
        print("{:<{width}}".format(column_names[i], width=column_widths[i]), end=" ")
    print("\n" + "-" * sum(column_widths))

    for row in rows:
        for i in range(len(row)):
            print("{:<{width}}".format(row[i], width=column_widths[i]), end=" ")
        print()
else:
    print("Немає результатів для цього запиту.")

# Порахувати кількість поставок від кожного постачальника
cur.execute("""
SELECT s.company_name, COUNT(d.delivery_id) AS total_deliveries
FROM suppliers s
LEFT JOIN deliveries d ON s.supplier_id = d.supplier_id
GROUP BY s.company_name;
""")
rows = cur.fetchall()

if rows:
    print("\nКількість поставок від кожного постачальника:")
    column_names = ["Назва постачальника", "Загальна кількість поставок"]
    column_widths = [25, 15]
    for i in range(len(column_names)):
        print("{:<{width}}".format(column_names[i], width=column_widths[i]), end=" ")
    print("\n" + "-" * sum(column_widths))

    for row in rows:
        for i in range(len(row)):
            print("{:<{width}}".format(row[i], width=column_widths[i]), end=" ")
        print()
else:
    print("Немає результатів для цього запиту.")

cur.close()
conn.close()
