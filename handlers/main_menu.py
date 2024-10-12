from aiogram import Router, F
from aiogram.types import Message
import asyncpg

from keyboards.menu_kb import menu_keyboard, buzzer_kb

router = Router()

buzzer_text = """
💻Дорогие воркеры, специально для вас, мы открыли новую возможность для улучшения вашей работоспособности!

🔥Теперь вам доступна официальная голосовая поддержка через звонок внутри телеграмм на любые ситуации от самых опытных и продвинутых девушек сферы прозвона.

🔵Гарантом качества и мастерства девушек служит многолетний опыт, особый подход к работе, а также отличное СИ.

✍️Условия сотрудничества просты - в случае профита взимается 2% за услугу поддержки голосом

🤝Инструкция по приему заявки на прозвон:
1. Анкету 
2. Информация по ключевым моментам с упоминанием важных деталей и допуск на аккаунт заранее, для изучения недавней переписки
3. Перечисление процедур, которые уже были у мамонта, в случае их наличия

В конце обращения «С правилами ознакомлен и согласен» 

⚠️ Уважаемые воркеры, ведите себя культурно в общении со стаффом. Заявки на тематики «просто поболтать/доказать реал/звонить не внутри телеграмм/видео звонки любого вида» и прочие не деловые заявки будут отклоняться.
"""

@router.message(F.text == "📂 Основное меню")
async def main_menu(message: Message):
    await message.answer(
        "🔽 Вот меню, выбирайте нужный пункт:", reply_markup=menu_keyboard()
    )
    
@router.message(F.text == "📞 Прозвон")
async def buzzer(message: Message):
    await message.answer("В разработке..")

@router.message(F.text == "📄 Проверка чеков")
async def check_verif(message: Message):
    await message.answer("В разработке..")

@router.message(F.text == "❗️ Жалоба на карты")
async def card_complaint(message: Message):
    await message.answer("В разработке..")

@router.message(F.text == "🫂 Наставники")
async def mentors(message: Message):
    await message.answer("В разработке..")

@router.message(F.text == "🌐 Полезное")
async def useful(message: Message):
    await message.answer("В разработке..")




