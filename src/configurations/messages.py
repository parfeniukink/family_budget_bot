from shared.messages import BOLD, CODE, LINE_ITEM

CONFIGURATION_UPDATED_MESSAGE = "\n".join(
    (
        "✅ Configuration updated",
        LINE_ITEM.format(key="{configuration_name}", value="{configuration_value}"),
    )
)

CONFIGURATION_WAS_NOT_FOUND_MESSAGE = "Can not find configuration {config_name} in database"

CONFIGURATION_UPDATE_PAYLOAD_INVALID_MESSAGE = "Invalid configuratoin update payload"

CONFIGURATION_VALUE_IS_NOT_SET_MESSAGE = "Configuration value is not set"

CONFIGURATION_INVALID_MESSAGE = "Invalid configuration selected"

CONFIGURATION_VALUE_VALUE_ERROR = "This value should be an integer"

CONFIGURATION_INCOME_SOURCE_PAYLOAD_ERROR = "\n".join(
    (
        "Invalid format. All configurations should match match next pattern:",
        CODE.format(text="value,value,value"),
        "",
        "Spaces not allowed between values. Use only comma.",
        "",
        "Example:",
        BOLD.format(text="My new job,Design"),
    )
)

CONFIGURATION_SELCT_MESSAGE = "Please, select the configuration ⬇️"

CONFIGURATION_ENTER_PROMPT = "Enter new value for configuration ⬇️"

CONFIGURATION_UPDATE_PAYLOAD_INVALID_MESSAGE = "Invalid configuratoin update payload"
