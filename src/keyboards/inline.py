from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

prediction_initial_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="На день", callback_data="prediction_initial_markup_daily"
            ),
            InlineKeyboardButton(
                text="Да/Нет", callback_data="prediction_initial_markup_bool"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Другое", callback_data="prediction_initial_markup_other"
            ),
        ],
    ]
)
