from db import database

with database.cursor() as cursor:
    cursor.execute("ALTER TABLE configurations ADD cost_sources VARCHAR(255)")
    cursor.execute("INSERT INTO categories (name) VALUES ('♥️ Health'), ('💼 Business')")
