from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

STUDENT = "Student"
TECHNOLOGIES = "IT-technologies"
CONTACTS = "Contacts"
PROMPT_AI = "Prompt AI"

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=STUDENT),
            KeyboardButton(text=TECHNOLOGIES),
        ],
        [
            KeyboardButton(text=CONTACTS),
            KeyboardButton(text=PROMPT_AI),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose action",
)