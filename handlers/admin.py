from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
import asyncpg
from db import db_main
from keyboards.admin_kb import admin_output_types, output_money
import re

router = Router()

@router.message(F.text == "🤖 Запросы на вывод")
async def output_requests(message: Message):
    conn = await db_main()

    await message.answer(
        "Выберите тип запроса.",
        reply_markup=admin_output_types()
    )
    await conn.close()

@router.message(F.text == "Ожидающие")
async def awaiting_requests(message: Message):
    conn = await db_main()

    existing_requests = await conn.fetch(
        "SELECT * FROM withdraw_request WHERE status = 'pending'"
    )

    if existing_requests:
        for request in existing_requests:
            user_stats = await conn.fetchrow(
                "SELECT * FROM user_stats WHERE user_id = $1", request['user_id']
            )
            if user_stats:
                await message.answer(
                    f"Запрос от пользователя @{request['username']}: {request['amount']} рублей.\n"
                    f"Кошелек пользователя: {user_stats['wallet']}", 
                    reply_markup=output_money()
                )
    else:
        await message.answer("Нет запросов.")
    
    await conn.close() 

@router.message(F.text == "Выполненные")
async def complete_requests(message: Message):
    conn = await db_main()

    existing_requests = await conn.fetch(
        "SELECT * FROM withdraw_request WHERE status = 'complete'"
    )

    if existing_requests:
        for request in existing_requests:
            user_stats = await conn.fetchrow(
                "SELECT * FROM user_stats WHERE user_id = $1", request['user_id']
            )
            if user_stats:
                await message.answer(
                    f"Запрос от пользователя @{request['username']}: {request['amount']} рублей.\n"
                    f"Кошелек пользователя: {user_stats['wallet']}", 
                    reply_markup=output_money()
                )
    else:
        await message.answer("Нет запросов.")
    
    await conn.close() 

@router.callback_query(F.data == "make_withdraw")
async def withdraw_handler(call: CallbackQuery):
    conn = await db_main()
    message_text = call.message.text

    match = re.search(r'@(\w+)', message_text)
    if match:
        username = match.group(1)

        user_data = await conn.fetchrow(
            "SELECT user_id FROM withdraw_request WHERE username = $1", username
        )
        if user_data:
            user_id = user_data['user_id']
            print(f"Найден user_id: {user_id}")
        else:
            await call.message.answer("Пользователь не найден.")
            await conn.close()
            return

        withdraw_request = await conn.fetchrow(
            "SELECT * FROM withdraw_request WHERE status = 'pending' AND user_id = $1", 
            user_id
        )

        if withdraw_request:
            user_stats = await conn.fetchrow(
                "SELECT * FROM user_stats WHERE user_id = $1",
                user_id
            )

            if user_stats and user_stats['balance'] >= withdraw_request['amount']:
                new_balance = user_stats['balance'] - withdraw_request['amount']

                await conn.execute(
                    """
                    UPDATE user_stats
                    SET balance = $1
                    WHERE user_id = $2
                    """,
                    new_balance, user_id
                )

                await conn.execute(
                    """
                    UPDATE withdraw_request
                    SET status = 'completed'
                    WHERE id = $1
                    """,
                    withdraw_request['id']
                )

                await call.message.answer(f"Запрос на вывод обработан. Новый баланс: {new_balance} рублей.")
            else:
                await call.message.answer("Недостаточно средств.")
                print(f"Текущий баланс: {user_stats['balance'] if user_stats else 'Не найден'}, "
                      f"Запрашиваемая сумма: {withdraw_request['amount']}")
        else:
            await call.message.answer("Запрос не найден.")
    else:
        await call.message.answer("Имя пользователя не указано в сообщении.")

    await conn.close()
