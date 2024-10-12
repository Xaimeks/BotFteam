from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def menu_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="👤 Профиль")
    kb.button(text="📞 Прозвон")
    kb.button(text="📄 Проверка чеков")
    kb.button(text="❗️ Жалоба на карты")
    kb.button(text="📨 Связь с администрацией")
    kb.button(text="🫂 Наставники")
    kb.button(text="🌐 Полезное")
    kb.adjust(2)
    
    return kb.as_markup(resize_keyboard=True)

def buzzer_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Перейти", url="https://www.google.com")
    kb.adjust(1)
    
    return kb.as_markup()