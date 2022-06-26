from db import database

with database.cursor() as cursor:
    cursor.execute("INSERT INTO categories (name) VALUES ('💸 Debts')")
