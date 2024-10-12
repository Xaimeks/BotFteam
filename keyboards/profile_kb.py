from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def profile_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="👤 Профиль")
    kb.button(text="💳 Оформить выплату")
    kb.button(text="⚙️ Настройки")
    kb.adjust(2)
    
    return kb.as_markup(resize_keyboard=True)

def profile_keyboard_inline() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="💳 Оформить выплату", callback_data="payment")
    kb.button(text="⚙️ Настройки", callback_data="settings")
    kb.adjust(2)
    
    return kb.as_markup(resize_keyboard=True)