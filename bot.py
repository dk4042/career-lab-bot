from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

from telegram.ext import MessageHandler, Filters
import os  

TOKEN = os.environ.get("BOT_TOKEN") 

menu_options = ['Paypal', 'Kaspi', 'Zelle', 'Перевод']

messages = {
    'Paypal': "Для оплаты с помощью Paypal, отправьте платеж на номер: 7735950933. Как только вы это сделаете, отправьте скриншот в этот чат.",
    'Kaspi': "Для оплаты с помощью Kaspi, отправьте платеж на номер: KIRILL FINANCE. Как только вы это сделаете, отправьте скриншот в этот чат.",
    'Zelle': "Для оплаты с помощью Zelle, отправьте платеж на номер: 7735950933. Как только вы это сделаете, отправьте скриншот в этот чат.",
    'Перевод': "Для оплаты переводом, отправьте платеж на номер: LIZA. Как только вы это сделаете, отправьте скриншот в этот чат."
}

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(option, callback_data=option)]
        for option in menu_options
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Добро пожаловать в Career Lab! Чтобы присоединиться к чату, выберите способ оплаты.",
        reply_markup=reply_markup
    )

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()  
    choice = query.data
    response = messages.get(choice, "Неизвестный способ.")
    # Send new message instead of editing
    keyboard = [
        [InlineKeyboardButton(option, callback_data=option)]
        for option in menu_options
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(
        chat_id=query.message.chat.id,
        text=response,
        reply_markup=reply_markup
    )


 
MODERATOR_CHAT_IDS = [5671154512, 391193896]

def photo_handler(update: Update, context: CallbackContext):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()  # Get highest-res photo
    os.makedirs('user_photos', exist_ok=True)        # Create folder if it doesn't exist
    file_path = f'user_photos/{user.id}_{photo_file.file_id}.jpg'
    photo_file.download(file_path)                    # Download photo locally

    # Reply to user
    update.message.reply_text("Спасибо за фото! Мы его получили. Добавим вас в чат Career Lab, как только сможем. Если возникла проблема и вас не добавили в течение 12 часов, пожалуйста, свяжитесь с Kirill Finance.")

    # Forward photo to moderators
    for mod_id in MODERATOR_CHAT_IDS:
        context.bot.send_photo(
            chat_id=mod_id,
            photo=open(file_path, 'rb'),
            caption=f"Photo from @{user.username or user.first_name} (ID: {user.id})"
        )
   
def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("Команды бота:\n/start — начать\n/help — помощь\n/info — информация о Career Lab")

def info_command(update: Update, context: CallbackContext):
    update.message.reply_text("Career Lab — это профессиональное коммьюнити для студентов и молодых специалистов. Чтобы присоединиться, Вам необходимо выбрать тариф (базовый или pro), и произвести оплату.")

def career_lab(update: Update, context: CallbackContext):
    update.message.reply_text("Этот тариф даёт вам: - доступ к 4-недельному курсу Career Lab (звонки в Zoom о том, как начать карьеру, узнать о финансах и консалтинге); - после завершения курса вы будете добавлены в сообщество, где вас ждут эксклюзивные нетворкинг- и образовательные мероприятия на всю жизнь.Чтобы попасть в Career Lab, пожалуйста, нажмите /start и следуйте инструкциям.")

def career_lab_pro(update: Update, context: CallbackContext):
    update.message.reply_text("Этот тариф даёт вам: - доступ к 4-недельному курсу Career Lab (звонки в Zoom о том, как начать карьеру, узнать о финансах и консалтинге); - после завершения курса вы будете добавлены в сообщество, где вас ждут эксклюзивные нетворкинг и образовательные мероприятия для всей жизни; - персональные и групповые консультации по составлению резюме и собеседованиям; - глубокое погружение в индустрии (мы проведём с вами собеседование по финансам и консалтингу);Чтобы попасть в Career Lab Pro, пожалуйста, нажмите /start и следуйте инструкциям.")

def command3(update: Update, context: CallbackContext):
    update.message.reply_text("CareerLab — навигатор в мир международной карьеры. Мы — Даша, Кирилл, и Лиза— объединили опыт в консалтинге, финансах и бизнесе, чтобы помочь тебе построить карьеру в топовых компаниях по всему миру. We came together to create a most comprehensive 4-week program that will allow you to headstart your career. Мы объединились, чтобы создать максимально полную 4-недельную программу, которая позволит вам быстро начать карьеру. Мы предлагаем доступную базовую версию, которая позволит вам освоить все основы. В версии Pro мы будем работать с вашим случаем более индивидуально. Оба потока получат доступ к сообществу после завершения курса. Готовы присоединиться? Тогда нажмите /start")

# Main function to run the bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('info', info_command))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(Filters.photo, photo_handler))
    dp.add_handler(CommandHandler("career_lab", career_lab))
    dp.add_handler(CommandHandler("career_lab_pro", career_lab_pro))
    dp.add_handler(CommandHandler("command3", command3))

    print("Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

