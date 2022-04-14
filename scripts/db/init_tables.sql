CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL,
    chat_id INTEGER NOT NULL,
    username VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS categories(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS costs(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    value NUMERIC NOT NULL,
    currency VARCHAR(3) NOT NULL,
    date DATE NOT NULL,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(category_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS incomes(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    value NUMERIC NOT NULL,
    currency VARCHAR(3) NOT NULL,
    date DATE NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);


INSERT INTO categories (name) VALUES
    ('Food'),
    ('Restaurants'),
    ('Roads'),
    ('Clothes'),
    ('Car'),
    ('Fuel'),
    ('Household'),
    ('Rents'),
    ('Services'),
    ('Leisure'),
    ('Technical stuff'),
    ('Other'),
    ('Currency transactions');
