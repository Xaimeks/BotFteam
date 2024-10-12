from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def start_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="👤 Профиль")
    kb.button(text="📂 Основное меню")
    kb.adjust(2)
    
    return kb.as_markup(resize_keyboard=True)