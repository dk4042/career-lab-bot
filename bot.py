import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ.get("BOT_TOKEN")

menu_options = ['Paypal', 'Kaspi', 'Zelle', 'Перевод']

messages = {
    'Paypal': "Для оплаты с помощью Paypal, отправьте платеж на номер: 7735950933. Как только вы это сделаете, отправьте скриншот в этот чат.",
    'Kaspi': "Для оплаты с помощью Kaspi, отправьте платеж на номер: KIRILL FINANCE. Как только вы это сделаете, отправьте скриншот в этот чат.",
    'Zelle': "Для оплаты с помощью Zelle, отправьте платеж на номер: 7735950933. Как только вы это сделаете, отправьте скриншот в этот чат.",
    'Перевод': "Для оплаты переводом, отправьте платеж на номер: LIZA. Как только вы это сделаете, отправьте скриншот в этот чат."
}

MODERATOR_CHAT_IDS = [5671154512]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(option, callback_data=option)]
        for option in menu_options
    ]
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
    keyboard = [
        [InlineKeyboardButton(option, callback_data=option)]
        for option in menu_options
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=query.message.chat.id,
        text=response,
        reply_markup=reply_markup
    )

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    os.makedirs('user_photos', exist_ok=True)
    file_path = f'user_photos/{user.id}_{photo_file.file_id}.jpg'
    await photo_file.download_to_drive(file_path)
    
    await update.message.reply_text(
        "Спасибо за фото! Мы его получили. Добавим вас в чат Career Lab, как только сможем. Если возникла проблема и вас не добавили в течение 12 часов, пожалуйста, свяжитесь с Kirill Finance."
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
        "Команды бота:\n/start — начать\n/help — помощь\n/info — информация о Career Lab"
    )

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Career Lab — это профессиональное коммьюнити для студентов и молодых специалистов. Чтобы присоединиться, Вам необходимо выбрать тариф (базовый или pro), и произвести оплату."
    )

async def career_lab(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Этот тариф даёт вам: - доступ к 4-недельному курсу Career Lab (звонки в Zoom о том, как начать карьеру, узнать о финансах и консалтинге); - после завершения курса вы будете добавлены в сообщество, где вас ждут эксклюзивные нетворкинг- и образовательные мероприятия на всю жизнь.Чтобы попасть в Career Lab, пожалуйста, нажмите /start и следуйте инструкциям."
    )

async def career_lab_pro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Этот тариф даёт вам: - доступ к 4-недельному курсу Career Lab (звонки в Zoom о том, как начать карьеру, узнать о финансах и консалтинге); - после завершения курса вы будете добавлены в сообщество, где вас ждут эксклюзивные нетворкинг и образовательные мероприятия для всей жизни; - персональные и групповые консультации по составлению резюме и собеседованиям; - глубокое погружение в индустрии (мы проведём с вами собеседование по финансам и консалтингу);Чтобы попасть в Career Lab Pro, пожалуйста, нажмите /start и следуйте инструкциям."
    )

async def command3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "CareerLab — навигатор в мир международной карьеры. Мы — Даша, Кирилл, и Лиза— объединили опыт в консалтинге, финансах и бизнесе, чтобы помочь тебе построить карьеру в топовых компаниях по всему миру. We came together to create a most comprehensive 4-week program that will allow you to headstart your career. Мы объединились, чтобы создать максимально полную 4-недельную программу, которая позволит вам быстро начать карьеру. Мы предлагаем доступную базовую версию, которая позволит вам освоить все основы. В версии Pro мы будем работать с вашим случаем более индивидуально. Оба потока получат доступ к сообществу после завершения курса. Готовы присоединиться? Тогда нажмите /start"
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    app.add_handler(CommandHandler("career_lab", career_lab))
    app.add_handler(CommandHandler("career_lab_pro", career_lab_pro))
    app.add_handler(CommandHandler("command3", command3))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()