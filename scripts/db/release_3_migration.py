from db import database

with database.cursor() as cursor:
    users = database.raw_execute("SELECT id from users")
    cursor.execute(r"DROP TABLE IF EXISTS configurations RESTRICT")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS configurations( "
        "id SERIAL PRIMARY KEY,"
        "default_currency VARCHAR(3) NOT NULL,"
        "income_sources VARCHAR(255),"
        "keyboard_dates_amount NUMERIC NOT NULL,"
        "user_id INTEGER NOT NULL,"
        "FOREIGN KEY(user_id) REFERENCES users(id))"
    )
    for user in users:
        cursor.execute(
            f"INSERT INTO configurations "
            f"(default_currency, keyboard_dates_amount, user_id) "
            f"VALUES ('byn', 5, {user['id']})"
        )
