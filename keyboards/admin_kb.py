from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def admin_start_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="👤 Профиль")
    kb.button(text="📂 Основное меню")
    kb.button(text="🤖 Запросы на вывод")
    kb.adjust(2)
    
    return kb.as_markup(resize_keyboard=True)

def admin_output_types() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="👤 Профиль")
    kb.button(text="Ожидающие")
    kb.button(text="Выполненные")
    kb.adjust(2)
    
    return kb.as_markup(resize_keyboard=True)

def output_money() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Сделать вывод", callback_data="make_withdraw")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


