from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
import asyncpg
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from db import db_main
from db import fetch_user_data
import re
from keyboards.for_start_kb import start_keyboard

router = Router()

class AmountSelection(StatesGroup):
    choosing_amount = State()

@router.callback_query(F.data == "payment")
async def payments_handler(call: CallbackQuery, state: FSMContext):
    await call.answer("Вы выбрали оплату")
    await call.message.answer(
        "Введите сумму которую вы хотите вывести:"
    )
    await state.set_state(AmountSelection.choosing_amount)

@router.message(StateFilter(AmountSelection.choosing_amount))
async def amount_entry(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username

    if not re.match(r'^\d+(\.\d+)?$', message.text):
        await message.answer("Введите корректное число.", reply_markup=start_keyboard())
        await state.clear()
        return

    amount = float(message.text)

    user_data = await fetch_user_data(user_id)

    if user_data:
        user_data = user_data[0] 
        balance = user_data['balance'] 
    else:
        await message.answer("Не удалось получить данные пользователя.", reply_markup=start_keyboard())
        return
    

    if amount < 1000:
        await message.answer("Вывод начинается от 1000 рублей.", reply_markup=start_keyboard())
        return

    if balance < amount:
        await message.answer(f"На вашем балансе недостаточно средств. Ваш баланс: {balance}.", reply_markup=start_keyboard())
        return

    conn = await db_main()
    try:
        existing_request = await conn.fetchrow(
            "SELECT * FROM withdraw_request WHERE user_id = $1 AND status = 'pending' ",
            user_id
        )
        if existing_request:
            await message.answer(
                "У вас уже есть неподтвержденный запрос на вывод.", reply_markup=start_keyboard()
            )
            await state.clear()
            return

        await conn.execute(
            """
            INSERT INTO withdraw_request (user_id, amount, status, username)
            VALUES ($1, $2, $3, $4)
            """,
            user_id, amount, 'pending', username
        )
        await message.answer(f"Ваш запрос на вывод {amount} рублей отправлен на рассмотрение.", reply_markup=start_keyboard())

    except Exception as e:
        await message.answer("Произошла ошибка при отправке запроса на вывод.", reply_markup=start_keyboard())
        print(f"Не получилось отправить запрос на вывод: {e}", reply_markup=start_keyboard())

    finally:
        await conn.close()

    await state.clear()
