from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup

main_menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Новое предсказание"),
        ],
    ],
    resize_keyboard=True,
    is_persistent=True,
)
