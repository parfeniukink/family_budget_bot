from shared.messages import LINE_ITEM

INCOME_TYPE_NOT_SELECTED_ERROR = "Income type option is not selected"
INCOME_OPTION_INVALID_ERROR = "Invalid income option. Please use the keyboard"
VALUE_NOT_ADDED_ERROR = "Value is not added"
DATE_NOT_SELECTED_ERROR = "Date is not selected"
DATE_INVALID_ERROR = "Invalid date"
MONTHLY_DATE_FORMAT_INVALID = "Invalid monthly date format"
YEAR_FORMAT_INVALID = "Invalid year. Year should be a number"

INCOME_SAVE_ERROR = "One or more mandatory values are not set"

INCOME_GET_NO_USER_ERROR = "For some reason there is not user in database related to this income {income}"

INCOME_DETAILED_ITEM_MESSAGE = "".join(
    (
        "{fdate}   {user}",
        " | ",
        LINE_ITEM.format(key="{income_name}", value="{income_value}"),
        "{sign}\n",
    )
)

TOTAL_INCOMES_LIST_MESSAGE = " ".join((LINE_ITEM.format(key="{title}", value="{total_incomes}"), "{sign}"))


INCOME_VALUE_ADDED_MESSAGE = "\n".join(
    (LINE_ITEM.format(key="✅ Value added", value="{value}"), "Now, please select the currency from the list")
)

INCOME_NAME_ADDED_MESSAGE = "\n".join(
    (LINE_ITEM.format(key="✅ Name added", value="{name}"), "Now, please, enter the value:")
)

INCOME_DATE_ADDED_MESSAGE = "\n".join(
    (LINE_ITEM.format(key="✅Date added", value="{date}"), "Now, please, enter the name:")
)


INCOME_IS_SALARY_PROMPT = "\n".join((LINE_ITEM.format(key="Currency", value="{currency}"), "Is it salary?"))

SELECT_DATE_PROMPT = "Please, select date from the list"

MONEY_VALUE_INVALID_ERROR = "Money value is invalid"

INCOME_SAVE_CONFIRMATION_MESSAGE = "\n".join(
    [
        "Would you like to save this income ❓\n",
        LINE_ITEM.format(key="Date", value="{date}"),
        LINE_ITEM.format(key="Description", value="{description}"),
        LINE_ITEM.format(key="Value", value="{value}"),
        LINE_ITEM.format(key="Currency", value="{currency}"),
        "{source}",
    ]
)


INCOME_SAVED_MESSAGE = "✅ Incomes saved"
INCOME_NOT_SAVED_MESSAGE = "❌ Incomes wasn't saved"
