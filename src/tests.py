import calendar
from pprint import pprint

from config import database
from costs.models import Cost

# date = "2022-04"

# year, month, *_ = date.split("-")
# dates_amount = calendar.monthrange(int(year), int(month))[1]


# date_from = "-".join((date, "01"))
# date_to = "-".join((date, str(dates_amount)))

# q = f"SELECT * FROM costs where date > '{date_from}' and date < '{date_to}'"

# data = database.raw_execute(q)
# results = [Cost(**d) for d in data]


data = database.raw_execute("SELECT date FROM costs WHERE date < '2021-01-01'")

print(data)
