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
    salary BOOLEAN DEFAULT false,
    date DATE NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS equity(
    id SERIAL PRIMARY KEY,
    currency VARCHAR(3) NOT NULL,
    value NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS configurations(
    id SERIAL PRIMARY KEY,
    default_currency VARCHAR(3) NOT NULL,
    income_sources VARCHAR(255),
    keyboard_dates_amount NUMERIC NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);


/* ************************ */
/* Database population */ 
/* ************************ */

INSERT INTO categories (name) VALUES
    ('🍽 Food'),
    ('🥗 Restaurants'),
    ('🍔 Food delivery'),
    ('🚌 Roads'),
    ('👚 Clothes'),
    ('🚙 Car'),
    ('⛽️ Fuel'),
    ('🪴 Household'),
    ('🤝 Rents'),
    ('💳 Services'),
    ('🏝 Leisure'),
    ('💻 Technical stuff'),
    ('📚 Education'),
    ('🎁 Gifts'),
    ('📦 Other'),
    ('🔄 Currency transactions');

INSERT INTO equity (currency, value) VALUES
    ('byn', 0.0),
    ('usd', 0.0);
