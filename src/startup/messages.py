from shared.messages import BOLD, ITALIC

USER_CREATED_MESSAGE = "\n".join(
    (
        "Hey there 😎",
        "Now you're in the database!",
        "\n",
        " ".join(("Let's have a quick guide about", BOLD.format(text="How to work with bot?"))),
        ITALIC.format(text="In progress..."),
    )
)

USER_EXISTS_MESSAGE = "Actually, you do not need to press /start command again"
