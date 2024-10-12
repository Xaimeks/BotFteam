from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
import asyncpg
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from keyboards.for_start_kb import start_keyboard
from keyboards.admin_contact import admin_contact_kb
from db import db_main

router = Router()

class UserRequest(StatesGroup):
    user_message_unban = State()
    user_message_staff = State()

@router.message(F.text == "📨 Связь с администрацией")
async def admin_contact(message: Message):
    await message.answer("Выберите нужное:", reply_markup=admin_contact_kb())

@router.callback_query(F.data == "unban_request")
async def unban_request(call: CallbackQuery, state: FSMContext):
    await call.answer("Заявка на разбан")
    await call.message.answer(
        "Опишите вашу проблему, почему вы были заблокированы?"
    )
    await state.set_state(UserRequest.user_message_unban)

@router.message(StateFilter(UserRequest.user_message_unban))
async def unban_request_text(message: Message, state: FSMContext):
    user_message = str(message.text)
    username = message.from_user.username
    
    if len(user_message) > 255:
        await message.answer("Слишком длинное сообщение")
        return 

    conn = await db_main()
    try:
        await conn.execute(
            """
            INSERT INTO unban_requests (user_name, request_text)
            VALUES ($1, $2)
            """,
            username, user_message
        )
        await message.answer("Ваш запрос на разблокировку отправлен.", reply_markup=start_keyboard())
    
    except Exception as e:
        await message.answer("Произошла ошибка при отправке запроса.", reply_markup=start_keyboard())
        print(f"Ошибка {e}")
    
    finally:
        await state.clear() 
        await conn.close()

@router.callback_query(F.data == "staff_request")
async def staff_request(call: CallbackQuery, state: FSMContext):
    await call.answer("Заявка в стафф проекта")
    conn = await db_main()
    user_id = call.from_user.id
    user_status = await conn.fetchrow(
        """
        SELECT status FROM user_stats WHERE user_id = $1
        """, user_id
    )
    if user_status == "GOLDEN" or "DIAMOND":
        await call.message.answer(
            "Расскажите о себе."
        )
        await state.set_state(UserRequest.user_message_staff)
    else:
        await call.message.answer(
            "Подать заявку в стафф можно только если у вас от 100к профита."
        )

@router.message(StateFilter(UserRequest.user_message_staff))
async def staff_request_text(message: Message, state: FSMContext):
    user_message = str(message.text)
    username = message.from_user.username
    
    if len(user_message) > 255:
        await message.answer("Слишком длинное сообщение")
        return 

    conn = await db_main()
    try:
        await conn.execute(
            """
            INSERT INTO staff_requests (username, request_text)
            VALUES ($1, $2)
            """,
            username, user_message
        )
        await message.answer("Ваш запрос в стафф команды отправлен.", reply_markup=start_keyboard())
    
    except Exception as e:
        await message.answer("Произошла ошибка при отправке запроса.", reply_markup=start_keyboard())
        print(f"Ошибка {e}")
    
    finally:
        await state.clear() 
        await conn.close()