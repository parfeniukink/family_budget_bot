BOLD = "<b>{text}</b>"
ITALIC = "<i>{text}</i>"
CODE = "<code>{text}</code>"

INDENTION = "    "

LINE_ITEM = "{key} 👉 {value}"

CURRENCY_INVALID_ERROR = "Currency invalid. Allowed: {allowed}"

INVAID_OPTION_MESSAGE = "Option invalid. Please use the keyboard"

BASE_QUESTION = "What do you want to do ?"

RESTART = "Keyboard restarted"

ABORTED = "⚠️ Aborted"

CATEGORY_SELECTED = "\n".join(
    (LINE_ITEM.format(key="✅ Category", value="{category} selected"), "Now, please, select the date 📅 from the list")
)
CATEGORY_NOT_SELECTED_ERROR = "❌ Category is not selected"
