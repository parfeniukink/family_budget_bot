from shared.messages import LINE_ITEM

INCOME_DETAILED_ITEM_MESSAGE = "".join(
    (
        "{fdate}   {user}",
        " | ",
        LINE_ITEM.format(key="{income_name}", value="{income_value}"),
        "{sign}\n",
    )
)

INCOME_GET_NO_USER_ERROR = "For some reason there is not user in database related to this income {income}"
MONTHLY_DATE_FORMAT_INVALID = "Invalid monthly date format"
TOTAL_INCOMES_LIST_MESSAGE = " ".join((LINE_ITEM.format(key="{title}", value="{total_incomes}"), "{sign}"))
YEAR_FORMAT_INVALID = "Invalid year. Year should be a number"
