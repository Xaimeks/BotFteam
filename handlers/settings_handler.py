from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
import asyncpg
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keyboards.settings_kb import settings_kb
from aiogram.filters import StateFilter
from db import db_main
from keyboards.for_start_kb import start_keyboard
from keyboards.settings_kb import payment_settings_kb

router = Router()

class FakeTagSettings(StatesGroup):
    fake_tag = State()

class PaymentSettings(StatesGroup):
    crypto_bot_wallet = State()
    usdt_wallet = State()
    card_number = State()

@router.callback_query(F.data == "settings")
async def settings_handler(call: CallbackQuery):
    conn = await db_main()
    user_id = call.message.from_user.id
    usdt_wallet = await conn.fetchval('SELECT usdt_trc_adress FROM user_stats WHERE user_id = $1', user_id)
    crypto_bot_wallet = await conn.fetchval('SELECT crypto_bot_wallet FROM user_stats WHERE user_id = $1', user_id)
    card_number = await conn.fetchval('SELECT card_number FROM user_stats WHERE user_id = $1', user_id)
    fake_tag = await conn.fetchval('SELECT fake_tag FROM user_stats WHERE user_id = $1', user_id)

    await call.answer("Вы выбрали настройки")
    await call.message.answer(
        "⚙️Настройки\n\n"
        f"USDT TRC-20: {usdt_wallet}\n"
        f"Crypto Bot: {crypto_bot_wallet}\n"
        f"Card Number: {card_number}\n"
        f"Ваш фейк тег: {fake_tag}\n",
        reply_markup=settings_kb()
    )

@router.message(F.text == "💳 Настройка выплат")
async def payment_settings(message: Message):
    await message.answer("🔽Способы вывода", reply_markup=payment_settings_kb())

@router.callback_query(F.data == "cryptobot")
async def crypto_bot_method(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Укажите ваш кошелек Crypto Bot в сети Tron")
    call.answer("Crypto Bot")
    await state.set_state(PaymentSettings.crypto_bot_wallet)

@router.message(StateFilter(PaymentSettings.crypto_bot_wallet))
async def crypto_bot_wallet_entry(message: Message, state: FSMContext):
    user_id = message.from_user.id
    wallet_address = message.text

    conn = await db_main()
    await conn.execute(
        """
        UPDATE user_stats
        SET crypto_bot_wallet = $1
        WHERE user_id = $2
        """,
        wallet_address, user_id
    )
    await conn.close()

    await message.answer("Кошелек установлен", reply_markup=start_keyboard())
    await state.clear()

@router.callback_query(F.data == "usdt")
async def usdt_method(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Укажите ваш кошелек для USDT в сети Tron")
    call.answer("Usdt TRC-20")
    await state.set_state(PaymentSettings.usdt_wallet)

@router.message(StateFilter(PaymentSettings.usdt_wallet))
async def usdt_wallet_entry(message: Message, state: FSMContext):
    user_id = message.from_user.id
    wallet_address = message.text

    conn = await db_main()
    await conn.execute(
        """
        UPDATE user_stats
        SET usdt_trc_adress = $1
        WHERE user_id = $2
        """,
        wallet_address, user_id
    )
    await conn.close()

    await message.answer("Кошелек USDT установлен", reply_markup=start_keyboard())
    await state.clear()

@router.callback_query(F.data == "card")
async def card_method(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Укажите номер вашей карты")
    call.answer("Card Number")
    await state.set_state(PaymentSettings.card_number)

@router.message(StateFilter(PaymentSettings.card_number))
async def card_number_entry(message: Message, state: FSMContext):
    user_id = message.from_user.id
    card_number = message.text

    conn = await db_main()
    await conn.execute(
        """
        UPDATE user_stats
        SET card_number = $1
        WHERE user_id = $2
        """,
        card_number, user_id
    )
    await conn.close()

    await message.answer("Номер карты установлен", reply_markup=start_keyboard())
    await state.clear()

@router.message(F.text == "✏️ Изменить фейк тег")
async def change_fake_tag(message: Message, state: FSMContext):
    await message.answer("Укажите ваш фейк тег")
    await state.set_state(FakeTagSettings.fake_tag)

@router.message(StateFilter(FakeTagSettings.fake_tag))
async def set_fake_tag(message: Message, state: FSMContext):
    user_id = message.from_user.id
    fake_tag = message.text

    if not fake_tag.startswith('@'):
        fake_tag = '@' + fake_tag

    conn = await db_main()
    await conn.execute(
        """
        UPDATE user_stats
        SET fake_tag = $1
        WHERE user_id = $2
        """,
        fake_tag, user_id
    )
    await conn.close()

    await message.answer("Тег установлен", reply_markup=start_keyboard())
    await state.clear()

@router.message(F.text == "❌ Выключить фейк тег")
async def disable_fake_tag(message: Message):
    user_id = message.from_user.id
    conn = await db_main()
    await conn.execute(
        """
        UPDATE user_stats
        SET fake_tag = 'Не установлен'
        WHERE user_id = $1
        """, 
        user_id
    )
    await conn.close()

    await message.answer("Фейк тег выключен", reply_markup=start_keyboard())
