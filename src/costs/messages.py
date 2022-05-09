COST_DESCRIPTION_ADDED_MESSAGE = "✅ Description added 👉 {description}\nNow, please, enter the value"

COST_ADD_CATEGORY_SELECT_PROMPT = "Please, select category from the list"

COST_ADD_CATEGORY_SELECTED_MESSAGE = "✅ Category 👉 {category} selected\nNow, please, select the date 📅 from the list"


COST_ADD_DATE_SELECTED_MESSAGE = "✅ Date selected 👉 {date}\nNow, please, enter the description"

COST_NOT_FOUND_FOR_CATEGORY_MESSAGE = "✅ No costs in {cost} category"

COST_ADD_CONFIRMATION_MESSAGE = "\n".join(
    [
        "Would you like to save this costs ❓\n",
        "Date 👉 {date}",
        "Category 👉 {category}",
        "Description 👉 {description}",
        "Value 👉 {value}",
    ]
)

COST_SAVED_MESSAGE = "✅ Costs saved"
COST_NOT_SAVED_MESSAGE = "❌ Costs wasn't added"


COST_DELETE_DATE_SELECTED_MESSAGE = "✅ Date selected 👉 {month}\nNow, please, select category"

COST_DELETE_CATEGORY_SELECTED_MESSAGE = (
    "✅ Category selected 👉 {category}\nNow, please, select the id to delete\n\n{costs}"
)

COST_DELETE_MONTH_SELECT_PROMPT = "Please, select month from the list"

COST_DELETED_MESSAGE = "✅ Cost removed"


NO_MONTH_SELECTED_ERROR = "⚠️ No month selected"
