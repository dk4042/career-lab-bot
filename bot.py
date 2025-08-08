# -*- coding: utf-8 -*-
from dotenv import load_dotenv
load_dotenv()

import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Token from environment
TOKEN = os.environ.get("BOT_TOKEN")
tz = pytz.timezone('Europe/Moscow')

if not TOKEN:
    logger.error("BOT_TOKEN environment variable is not set. Exiting.")
    raise SystemExit("BOT_TOKEN not set")

menu_options = ['Paypal', 'Kaspi', 'Zelle', 'Перевод']

messages = {
    'Paypal': (
        "Для оплаты с помощью Paypal, отправьте платеж на номер: 7735950933. "
        "Как только вы это сделаете, отправьте скриншот в этот чат. "
        "При оплате, пожалуйста, укажите в сообщении ваш тег в Telegram."
    ),
    'Kaspi': (
        "Для оплаты с помощью Kaspi, отправьте платеж на номер: KIRILL FINANCE. "
        "Как только вы это сделаете, отправьте скриншот в этот чат. "
        "При оплате, пожалуйста, укажите в сообщении ваш тег в Telegram."
    ),
    'Zelle': (
        "Для оплаты с помощью Zelle, отправьте платеж на номер: 7735950933. "
        "Как только вы это сделаете, отправьте скриншот в этот чат. "
        "При оплате, пожалуйста, укажите в сообщении ваш тег в Telegram."
    ),
    'Перевод': (
        "Для оплаты переводом, отправьте платеж на номер:\n"
        " 4276380162792514 (Сбербанк),\n"
        " Наталия Александровна Волкова,\n"
        " 89150648677\n"
        "Как только вы это сделаете, отправьте скриншот в этот чат. "
        "При оплате, пожалуйста, укажите в сообщении ваш тег в Telegram."
    )
}

MODERATOR_CHAT_IDS = [5671154512, 391193896]

# Handlers (async for v20+)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(option, callback_data=option)] for option in menu_options]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Добро пожаловать в Career Lab! Чтобы присоединиться к чату, выберите способ оплаты.",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data
    response = messages.get(choice, "Неизвестный способ.")
    keyboard = [[InlineKeyboardButton(option, callback_data=option)] for option in menu_options]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=query.message.chat.id, text=response, reply_markup=reply_markup)

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    if not update.message.photo:
        await update.message.reply_text("Похоже, вы не отправили фото.")
        return

    photo_file = await update.message.photo[-1].get_file()
    os.makedirs('user_photos', exist_ok=True)
    file_path = f'user_photos/{user.id}_{photo_file.file_id}.jpg'
    await photo_file.download_to_drive(file_path)

    await update.message.reply_text(
        "Спасибо за фото! Мы его получили. Добавим вас в чат Career Lab, как только сможем. "
        "Если возникла проблема и вас не добавили в течение 12 часов, пожалуйста, свяжитесь с @dash_kham."
    )

    for mod_id in MODERATOR_CHAT_IDS:
        with open(file_path, 'rb') as photo:
            await context.bot.send_photo(
                chat_id=mod_id,
                photo=photo,
                caption=f"Photo from @{user.username or user.first_name} (ID: {user.id})"
            )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Команды бота:\n"
        "/start — начать\n"
        "/help — помощь\n"
        "/info — информация о Career Lab"
    )

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Career Lab — это профессиональное коммьюнити для студентов и молодых специалистов. "
        "Чтобы присоединиться, Вам необходимо выбрать тариф (базовый или pro), и произвести оплату. "
        " Готовы присоединиться? Выберите /start"
    )

async def career_lab(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Этот тариф даёт вам:\n"
        " - Доступ к 4-недельному курсу Career Lab (4 модуля: выбор карьеры, составление резюме, networking, deep dive в финансы/консалтинг)\n"
        " - Zoom-разбор с нами (мы — Лиза, Кирилл и Даша)\n"
        " - Приглашенные спикеры из индустрии (финансы, консалтинг, Big4, ООН, стартапы и не только)\n"
        " - Приглашение в закрытое Community после завершения курса\n"
        " Готовы присоединиться? Выберите /start\n"
    )

async def career_lab_pro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Career Lab Pro, помимо базового 4-недельного курса, включает в себя:\n"
        " - Групповые звонки по подготовке к интервью (финансы, консалтинг, поведенческие)\n"
        " - Практика кейсов и технических вопросов\n"
        " Готовы присоединиться? Выберите /start\n"
    )

async def command3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Career Lab — это профессиональное коммьюнити для студентов и молодых специалистов. Мы — Лиза, Кирилл и Даша, собрали самые полезные ресурсы и объединили наш опыт и знания, чтобы помочь вам приобрести необходимые навыки."
        "Чтобы присоединиться, Вам необходимо выбрать тариф (базовый или pro), и произвести оплату." 
        "Выберите /start"
    )

def main():
    scheduler = AsyncIOScheduler(timezone=tz)
    app = ApplicationBuilder().token(TOKEN).build()
    app.job_queue.scheduler = scheduler

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    app.add_handler(CommandHandler("career_lab", career_lab))
    app.add_handler(CommandHandler("career_lab_pro", career_lab_pro))
    app.add_handler(CommandHandler("command3", command3))

    logger.info("Bot is starting (polling)...")
    app.run_polling()

if __name__ == '__main__':
    main()
