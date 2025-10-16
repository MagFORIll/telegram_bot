# bot.py
from os import getenv
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
import asyncio

from models import init_db
from models.db import SessionLocal
from parsers.auto_ru import AutoRu

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()


class PreferencesForm(StatesGroup):
    brand = State()
    model = State()
    mileage = State()
    price = State()
    year = State()


markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Задать предпочтения")],
        [KeyboardButton(text="Просмотр предпочтений")],
        [KeyboardButton(text="Найти")]
    ],
    resize_keyboard=True
)


def parse_number(text: str) -> int | None:
    """Преобразует строку в число, убирая пробелы и проверяя корректность."""
    clean = text.replace(" ", "").replace("\u00A0", "")
    return int(clean) if clean.isdigit() else None


@dp.message(CommandStart())
async def start(message: Message):
    from models.db import SessionLocal
    import models.crud as crud

    db = SessionLocal()
    try:
        user = crud.get_user_by_telegram_id(db, message.from_user.id)
        if not user:
            crud.create_user(db, message.from_user.id, message.from_user.full_name)
    finally:
        db.close()
    await message.answer(
        f"Привет, {message.from_user.first_name}!",
        reply_markup=markup
    )

@dp.message(F.text == "Найти")
async def get_preferences(message: Message):
    from parsers import auto_ru
    import models.crud as crud


    db = SessionLocal()
    try:
        user_preferences = crud.get_preferences(
            db,
            telegram_id=message.from_user.id
        )
        parser = AutoRu(preferences=user_preferences, limit=5)
        cars = parser.parse()
        parser.close()

        await message.answer(f'Найдено {len(cars)} автомобилей:\n' + '\n'.join([f"{c['maker']} {c['model']} - {c['year']} - {c['price']}" for c in cars]))

    finally:
        db.close()


@dp.message(F.text == "Просмотр предпочтений")
async def get_preferences(message: Message):
    from models.db import SessionLocal
    import models.crud as crud

    db = SessionLocal()
    try:
        user_preferences = crud.get_preferences(
            db,
            telegram_id=message.from_user.id
        )
        await message.answer(f"✅ Ваши предпочтения:\n"
                             f"Марка: {user_preferences['brand']}\n"
                             f"Модель: {user_preferences['model']}\n"
                             f"Пробег: {user_preferences['mileage']} км\n"
                             f"Цена: {user_preferences['price']} ₽\n"
                             f"Год: {user_preferences['year']}")
    finally:
        db.close()

@dp.message(F.text == "Задать предпочтения")
async def ask_brand(message: Message, state: FSMContext):
    await message.answer("Введите марку автомобиля:")
    await state.set_state(PreferencesForm.brand)


@dp.message(PreferencesForm.brand)
async def process_brand(message: Message, state: FSMContext):
    await state.update_data(brand=message.text)
    await message.answer("Введите модель:")
    await state.set_state(PreferencesForm.model)


@dp.message(PreferencesForm.model)
async def process_model(message: Message, state: FSMContext):
    await state.update_data(model=message.text)
    await message.answer("Введите пробег:")
    await state.set_state(PreferencesForm.mileage)


@dp.message(PreferencesForm.mileage)
async def process_mileage(message: Message, state: FSMContext):
    mileage = parse_number(message.text)
    if mileage is None:
        await message.answer("Пробег должен быть числом")
        return
    await state.update_data(mileage=mileage)
    await message.answer("Введите цену:")
    await state.set_state(PreferencesForm.price)


@dp.message(PreferencesForm.price)
async def process_price(message: Message, state: FSMContext):
    price = parse_number(message.text)
    if price is None:
        await message.answer("Цена должна быть числом")
        return
    await state.update_data(price=price)
    await message.answer("Введите год выпуска:")
    await state.set_state(PreferencesForm.year)


@dp.message(PreferencesForm.year)
async def process_year(message: Message, state: FSMContext):
    if message.text.isdigit() and len(message.text) == 8:
        await message.answer("Год должен состоять из 4 цифр")
        return

    await state.update_data(year=int(message.text))
    data = await state.get_data()

    from models.db import SessionLocal
    import models.crud as crud

    db = SessionLocal()
    try:
        crud.update_user_preferences(
            db,
            telegram_id=message.from_user.id,
            preferences=data
        )
    finally:
        db.close()

    await message.answer(f"✅ Ваши предпочтения:\n"
                         f"Марка: {data['brand']}\n"
                         f"Модель: {data['model']}\n"
                         f"Пробег: {data['mileage']} км\n"
                         f"Цена: {data['price']} ₽\n"
                         f"Год: {data['year']}")
    await state.clear()


async def main():
    try:
        await dp.start_polling(bot, timeout=60, request_timeout=60)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    init_db()
    asyncio.run(main())
