from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def admin_contact_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Feedback", callback_data="feedback")
    kb.button(text="Подать заявку на разбан", callback_data="unban_request")
    kb.button(text="Подать заявку в стафф проекта", callback_data="staff_request")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)