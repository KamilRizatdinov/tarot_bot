import asyncio
import logging
import sys
import config

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from database import init_db
from models.user import User
from models.dialog import Dialog
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.regular import main_menu_markup
from keyboards.inline import prediction_initial_markup
from aiogram import F

dp = Dispatcher()


class PredictionConfigurationState(StatesGroup):
    initial = State()
    type = State()
    cards = State()


class PredictionState(StatesGroup):
    initial = State()
    configuration = PredictionConfigurationState()
    inference = State()


class MainState(StatesGroup):
    initial = State()
    prediction = PredictionState()


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    user = await User.get_or_create(
        telegram_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
        language_code=message.from_user.language_code,
    )

    await state.set_state(MainState.initial)
    await message.answer(
        f"Здравствуй, {user.first_name}! Добро пожаловать к величайшей гадалке всех времен!!!",
        reply_markup=main_menu_markup,
    )


@dp.message(F.text == "Новое предсказание")
async def message_start_prediction_handler(message: Message, state: FSMContext) -> None:
    user = await User.find_one({"telegram_id": message.from_user.id})

    if not user:
        return

    await Dialog.get_or_create(telegram_id=message.from_user.id)
    await state.set_state(PredictionState.initial)
    await message.answer(
        "Выберите тип предсказания.", reply_markup=prediction_initial_markup
    )


@dp.callback_query(PredictionState.initial, F.data == "prediction_initial_markup_daily")
async def callback_query_prediction_initial_markup_daily_handler(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    print(await state.get_state())
    await state.set_state(PredictionConfigurationState.cards)
    await callback_query.message.answer("Предсказание на сегодня")


@dp.callback_query(PredictionState.initial, F.data == "prediction_initial_markup_bool")
async def callback_query_prediction_initial_markup_bool_handler(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    print(await state.get_state())
    await state.set_state(PredictionConfigurationState.cards)
    await callback_query.message.answer(
        "Предсказание с исходом да/нет",
    )


@dp.callback_query(PredictionState.initial, F.data == "prediction_initial_markup_other")
async def callback_query_prediction_initial_markup_other_handler(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    print(await state.get_state())
    await state.set_state(PredictionConfigurationState.type)
    await callback_query.message.answer("Другое предсказание")


@dp.message(PredictionState.initial)
async def message_prediction_initial_handler(
    message: Message, state: FSMContext
) -> None:
    user = await User.find_one({"telegram_id": message.from_user.id})

    if not user:
        return

    await Dialog.get_or_create(telegram_id=message.from_user.id)
    await message.answer(
        "Пожалуйста, выберите тип предсказания.", reply_markup=prediction_initial_markup
    )


async def main() -> None:
    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
