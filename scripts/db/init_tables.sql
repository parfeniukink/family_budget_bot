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
    cost_sources VARCHAR(255),
    keyboard_dates_amount NUMERIC NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);


/* ************************ */
/* Database population */ 
/* ************************ */

INSERT INTO categories (name) VALUES
    ('ð― Food'),
    ('ðĨ Restaurants'),
    ('ð Food delivery'),
    ('ð Roads'),
    ('ð Clothes'),
    ('ð Car'),
    ('â―ïļ Fuel'),
    ('ðŠī Household'),
    ('âĨïļ Health'),
    ('ðĪ Rents'),
    ('ðģ Services'),
    ('ð Leisure'),
    ('ðŧ Technical stuff'),
    ('ð Education'),
    ('ð Gifts'),
    ('ðĶ Other'),
    ('ðž Business'),
    ('ðļ Debts'),
    ('ð Currency transactions');

INSERT INTO equity (currency, value) VALUES
    ('uah', 0.0),
    ('usd', 0.0);
