from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
import asyncpg
from db import fetch_user_data
from keyboards.profile_kb import profile_keyboard, profile_keyboard_inline

def get_profile_text(user_name: str, user_id: int, status: str, percent: float, balance: float, daily_profit: float, monthly_profit: float, total_profit: float, fake_tag: str) -> str:
    return f"""⚡️ Профиль: @{user_name}
👤 ID: {user_id}
🔎 Fake тег: {fake_tag}
⚜️ Статус: {status}
💠 Ваш процент: {percent}%

💳 Ваш кошелёк
 Баланс: {balance}₽

🥳 Ваши профиты 
┣ За день: {daily_profit}₽
┣ За месяц: {monthly_profit}₽ 
┗ За все время: {total_profit}₽"""

router = Router()

async def send_profile_info(message: Message):
    user_id = message.from_user.id

    user_data = await fetch_user_data(user_id)

    if user_data and len(user_data) > 0:
        user_data = user_data[0]

        user_name = user_data['username']
        status = user_data['status']
        percent = user_data['percent']
        balance = user_data['balance']
        daily_profit = user_data['daily_profit']
        monthly_profit = user_data['monthly_profit']
        total_profit = user_data['total_profit']
        fake_tag = user_data['fake_tag']

        profile_text = get_profile_text(user_name, user_id, status, percent, balance, daily_profit, monthly_profit, total_profit, fake_tag)

        await message.answer(
            profile_text,
            reply_markup=profile_keyboard_inline()
        )
    else:
        await message.answer("Пользователь не найден или возникла ошибка.")

@router.message(F.text == "👤 Профиль")
async def cmd_profile(message: Message):
    user_id = message.from_user.id
    await message.answer("🔽Вот ваш профиль", reply_markup=None)
    await send_profile_info(message)

@router.callback_query(F.data == "profile")
async def callback_profile(call: CallbackQuery):
    user_id = call.from_user.id
    await call.answer("Ваш профиль")
    await call.message.answer("🔽Вот ваш профиль", reply_markup=None)
    await send_profile_info(call.message)
