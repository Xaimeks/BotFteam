from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def settings_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="👤 Профиль")
    kb.button(text="💳 Настройка выплат")
    kb.button(text="✏️ Изменить фейк тег")
    kb.button(text="❌ Выключить фейк тег")
    kb.adjust(2)
    
    return kb.as_markup(resize_keyboard=True)

def payment_settings_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🪙 Crypto Bot", callback_data="cryptobot")
    kb.button(text="💳 Карта", callback_data="card")
    kb.button(text="🤖 USDT TRC-20", callback_data="usdt")
    kb.adjust(2)

    return kb.as_markup(resize_keyboard=True)