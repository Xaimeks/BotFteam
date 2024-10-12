from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import asyncpg
from os import getenv
from dotenv import load_dotenv

from keyboards.for_start_kb import start_keyboard
from keyboards.admin_kb import admin_start_keyboard
from db import insert_user_data
router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):

    user_id = message.from_user.id
    username = message.from_user.username

    await insert_user_data(user_id, username)

    load_dotenv()
    admin_username = getenv('ADMIN_USERNAME')

    if message.from_user.username == admin_username:
        await message.answer(
            "Вы администратор",
            reply_markup=admin_start_keyboard()
        ) 
    else:
        await message.answer(
            "1Win Team приветствует вас.",
            reply_markup=start_keyboard()
        ) 