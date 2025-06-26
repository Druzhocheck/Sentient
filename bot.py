import telebot
from telebot import types

# Инициализация бота с вашим токеном
bot = telebot.TeleBot("8042449400:AAGFepJ5TMj2RHEWIGe41W3iUFLAgTk8Kcc")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Создаем клавиатуру с кнопкой News
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    news_button = types.KeyboardButton("News")
    markup.row(news_button)
    # Приветственное сообщение с emoji и HTML-разметкой
    WELCOME_MESSAGE = f"""
    ✨ <b>🌟 Dear {message.from_user.first_name} {message.from_user.last_name} 🌟</b> ✨

    🎊 <i>Welcome to our amazing Telegram bot!</i> 🎊

    📚 Here you'll discover:
    • The <b>freshest news</b> from Crypto world 🌍
    • <b>Curated content</b> tailored just for you ✨
    • <b>Daily updates</b> to keep you informed 📆

    🔥 <b>Hot features:</b>
    - Instant news notifications 🔔
    - Personalized news feed 🗞️
    - Trending stories analysis 📊

    👇 <b>Get started now!</b> 👇
    Press the <b>[ 🌟 News ]</b> button below to explore today's top stories!

    💡 <i>Stay informed</i>.

    ❤️ We're thrilled to have you with us! ❤️
    """
    # Отправляем приветственное сообщение
    bot.send_message(
        message.chat.id,
        WELCOME_MESSAGE,
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "News":
        show_categories(message)
    else:
        bot.send_message(message.chat.id, "Используйте кнопки для навигации")

def show_categories(message):
    markup = types.InlineKeyboardMarkup()
    
    # Создаем inline-кнопки с callback_data
    btn1 = types.InlineKeyboardButton("Vulnerabilities", callback_data="vulnerabilities")
    btn2 = types.InlineKeyboardButton("Hacking", callback_data="hacking")
    btn3 = types.InlineKeyboardButton("Laws", callback_data="laws")
    btn4 = types.InlineKeyboardButton("Investments and Funds", callback_data="investments")
    btn5 = types.InlineKeyboardButton("Mainnet", callback_data="mainnet")
    btn6 = types.InlineKeyboardButton("Airdrop", callback_data="airdrop")
    btn7 = types.InlineKeyboardButton("Mass Layoffs", callback_data="layoffs")
    btn8 = types.InlineKeyboardButton("Mergers", callback_data="mergers")
    btn9 = types.InlineKeyboardButton("Technica Innovations", callback_data="innovations")
    btn10 = types.InlineKeyboardButton("Своя категория", callback_data="custom_category")
    btn_back = types.InlineKeyboardButton("Назад", callback_data="back")
    
    # Распределяем кнопки по рядам
    markup.row(btn1)
    markup.row(btn2, btn3)
    markup.row(btn4, btn5)
    markup.row(btn6, btn7)
    markup.row(btn8, btn9)
    markup.row(btn10)
    markup.row(btn_back)
    
    bot.send_message(
        message.chat.id,
        'Выберите категорию новостей или введите свою',
        reply_markup=markup
    )

def go_back_to_main_menu(call):
    # Удаляем сообщение с inline-кнопками
    bot.delete_message(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )

# Обработчик inline-кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "back":
        pass
    elif call.data == "innovations":
        bot.send_message(
            call.message.chat.id,
            "Innovations",
        )
    elif call.data == "custom_category":
        # Обработка выбора своей категории
        msg = bot.send_message(
            call.message.chat.id,
            "Write down what kind of news you would like to recive."
        )
        bot.register_next_step_handler(msg, process_custom_category)
    go_back_to_main_menu(call)

def process_custom_category(message):
    bot.send_message(
        message.chat.id,
        #f"Вы создали категорию: {message.text}\nТеперь можно добавить новости в эту категорию."
    )
    show_categories(message)

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()