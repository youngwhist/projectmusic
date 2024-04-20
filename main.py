import os
import sqlite3

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackContext

from bass import bass_boost
from fast_or_slow import slowfast_music
BOT_TOKEN = "6760985613:AAEYf8uj5RWPXQiGQRhs2j3YjFpUbhBhOck"
# ссылка на бота https://t.me/forsoul_music_bot

# Состояния
REGISTER, LOGIN, WAITING_FOR_AUDIO, WAITING_FOR_INT_VALUE = range(4)

# База данных
conn = sqlite3.connect('users.sqlite')
cursor = conn.cursor()

# Клавиатуры
start_markup = ReplyKeyboardMarkup([['/register', '/login']], one_time_keyboard=True)
help_markup = ReplyKeyboardMarkup([['/how_use_bot', '/about'], ['/close']], one_time_keyboard=False)
main_menu_markup = ReplyKeyboardMarkup([['/start_redact', '/help'], ['/logout']], one_time_keyboard=False)


# Блок кода с регистрацией и авторизацией
# --------------------------------------------------------------------------------------------------------------------

async def start(update: Update, context: CallbackContext):
    if 'logged_in' in context.user_data and context.user_data['logged_in']:
        await update.message.reply_text(
            "Вы уже вошли в систему. Если вы хотите зарегистрировать новый аккаунт, сначала выйдите из текущего.")
        return ConversationHandler.END
    await update.message.reply_text("Добро пожаловать! Выберите /login для входа или /register для регистрации.")
    return ConversationHandler.END


# Функция для регистрации пользователя
async def register(update: Update, context: CallbackContext):
    if 'logged_in' in context.user_data and context.user_data['logged_in']:
        await update.message.reply_text(
            "Вы уже вошли в систему. Если вы хотите зарегистрировать новый аккаунт, сначала выйдите из текущего.")
        return ConversationHandler.END
    await update.message.reply_text("Введите имя пользователя и пароль через пробел:")
    return REGISTER


# Функция для обработки регистрации
async def handle_register(update, context):
    user_input = update.message.text.split()
    if update.message.text == "/exit":
        return await exit_process(update, context)
    if len(user_input) != 2:
        await update.message.reply_text("Неверный формат ввода. Попробуйте еще раз или введите /exit для выхода.")
        return REGISTER

    login, password = user_input
    # Проверка на существование логина
    cursor.execute("SELECT * FROM users WHERE login=?", (login,))
    if cursor.fetchone() is not None:
        await update.message.reply_text("Пользователь с таким логином уже существует. Попробуйте другой логин.")
        return REGISTER

    # Добавление пользователя в базу данных
    cursor.execute("INSERT INTO users (login, hashed_password) VALUES (?, ?)", (login, password))
    conn.commit()
    await update.message.reply_text("Регистрация успешно завершена!")
    return ConversationHandler.END


# Функция для входа пользователя
async def login(update: Update, context: CallbackContext):
    if 'logged_in' in context.user_data and context.user_data['logged_in']:
        await update.message.reply_text("Вы уже вошли в систему.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Введите имя пользователя и пароль через пробел:")
        return LOGIN


# Функция для обработки логина
async def handle_login(update, context):
    user_input = update.message.text.split()
    if update.message.text == "/exit":
        return await exit_process(update, context)
    if len(user_input) != 2:
        await update.message.reply_text("Неверный формат ввода. Попробуйте еще раз или введите /exit для выхода.")
        return LOGIN

    login, password = user_input
    # Проверка логина и пароля
    cursor.execute("SELECT * FROM users WHERE login=? AND hashed_password=?", (login, password))
    if cursor.fetchone() is not None:
        await update.message.reply_text("Вход успешно выполнен!", reply_markup=main_menu_markup)
        context.user_data['logged_in'] = True
        return ConversationHandler.END

    else:
        await update.message.reply_text("Неверный логин или пароль. Попробуйте еще раз или введите /exit для выхода.")
        return LOGIN


async def exit_process(update, context):
    await update.message.reply_text("Выход из процесса регистрации или входа...", reply_markup=start_markup)
    return ConversationHandler.END


# Конец блока кода
# ---------------------------------------------------------------------------------------------------------------------

# Блок кода с "каркасом" бота (logout, help)
# ---------------------------------------------------------------------------------------------------------------------

async def help(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Узнать как пользоваться ботом: /how_use_bot. Узнать о проекте: /about. Выйти: /close",
        reply_markup=help_markup
    )


async def how_use_bot(update: Update, context: CallbackContext):
    await update.message.reply_text("Тут текст как юзать бота")


async def about(update: Update, context: CallbackContext):
    await update.message.reply_text("Тут текст о проекте")


async def close(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Выберите опцию:",
        reply_markup=main_menu_markup
    )


async def logout(update: Update, context: CallbackContext):
    # Сброс состояния пользователя
    context.user_data.clear()
    # Установка флага logged_in в False
    context.user_data['logged_in'] = False
    await update.message.reply_text("Вы вышли из системы.", reply_markup=start_markup)
    return ConversationHandler.END


# Конец блока кода
# --------------------------------------------------------------------------------------------------------------------

# Блок кода с функциями
# --------------------------------------------------------------------------------------------------------------------

async def start_redact(update, context):
    redact_markup = ReplyKeyboardMarkup([
        ['/ekvalaizer', '/reverb', '/slow_fast'],
        ['/effect', '/noise_delete', '/gross_beat'],
        ['/bass', '/vocal_and_music'],
        ['/close']
    ], one_time_keyboard=False)

    await update.message.reply_text(
        "Выберите опцию для редактирования:",
        reply_markup=redact_markup
    )


async def ekvalaizer(update, context):
    await update.message.reply_text("Эквалайзер")


async def reverb(update, context):
    await update.message.reply_text("Ревёрб")


async def slow_fast(update, context):
    await update.message.reply_text(
        "Привет! Пришли мне звуковой файл."
    )
    return WAITING_FOR_AUDIO


async def bass(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Привет! Пришли мне звуковой файл."
    )
    return WAITING_FOR_AUDIO


# Функция для обработки аудиофайлов
async def handle_audio(update: Update, context: CallbackContext) -> int:
    audio_file = update.message.audio
    if audio_file:
        # Получаем файл ID
        file_id = audio_file.file_id
        # Используем файл ID для получения файла
        new_file = await context.bot.get_file(file_id)
        # Скачиваем файл
        local_file_path = await new_file.download_to_drive('audio.wav')
        # Сохраняем путь к локальному файлу в user_data для дальнейшего использования
        context.user_data['audio_file_path'] = local_file_path
        await update.message.reply_text("Спасибо! Теперь введи целое число.")
        return WAITING_FOR_INT_VALUE
    else:
        await update.message.reply_text("Пожалуйста, пришли звуковой файл.")
        return WAITING_FOR_AUDIO


# Функция для обработки целочисленных значений
async def handle_int_value_bass(update: Update, context: CallbackContext) -> int:
    int_value = update.message.text
    # Получаем путь к локальному файлу
    local_file_path = str(context.user_data.get('audio_file_path'))

    boosted_file_path = bass_boost(local_file_path, local_file_path, int_value)
    if local_file_path:
        # Отправляем аудиофайл пользователю
        with open(boosted_file_path, 'rb') as audio_file:
            await update.message.reply_audio(audio=audio_file)
        # Удаляем файл с локального диска
        os.remove(local_file_path)
    else:
        await update.message.reply_text("Не удалось найти аудиофайл для отправки.")

    return ConversationHandler.END


async def handle_int_value_slowfast(update: Update, context: CallbackContext) -> int:
    int_value = update.message.text
    # Получаем путь к локальному файлу
    local_file_path = str(context.user_data.get('audio_file_path'))

    boosted_file_path = slow_fast(local_file_path, int_value)
    if local_file_path:
        # Отправляем аудиофайл пользователю
        with open(boosted_file_path, 'rb') as audio_file:
            await update.message.reply_audio(audio=audio_file)
        # Удаляем файл с локального диска
        os.remove(local_file_path)
    else:
        await update.message.reply_text("Не удалось найти аудиофайл для отправки.")

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Операция отменена.')
    return ConversationHandler.END


async def vocal_and_music(update, context):
    await update.message.reply_text("Музыка и звук")


async def effect(update, context):
    await update.message.reply_text("Добавление эффектов")


async def noise_delete(update, context):
    await update.message.reply_text("Удаление шума")


async def gross_beat(update, context):
    await update.message.reply_text("Гросс бит")


async def close_redact(update, context):
    await update.message.reply_text(
        "Выберите опцию:",
        reply_markup=main_menu_markup
    )


# Конец блока кода
# --------------------------------------------------------------------------------------------------------------------

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Обработчики для регистрации и входа
    register_handler = ConversationHandler(
        entry_points=[CommandHandler("register", register)],
        states={
            REGISTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_register)]
        },
        fallbacks=[]
    )

    login_handler = ConversationHandler(
        entry_points=[CommandHandler("login", login)],
        states={
            LOGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_login)]
        },
        fallbacks=[]
    )

    conv_handler_bass = ConversationHandler(
        entry_points=[CommandHandler('bass', bass)],
        states={
            WAITING_FOR_AUDIO: [MessageHandler(filters.AUDIO, handle_audio)],
            WAITING_FOR_INT_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_int_value_bass)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    conv_handler_slow_fast = ConversationHandler(
        entry_points=[CommandHandler('slow_fast', slow_fast)],
        states={
            WAITING_FOR_AUDIO: [MessageHandler(filters.AUDIO, handle_audio)],
            WAITING_FOR_INT_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_int_value_slowfast)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )


    # Обработчики
    application.add_handler(register_handler)
    application.add_handler(login_handler)
    application.add_handler(conv_handler_bass)
    application.add_handler(conv_handler_slow_fast)
    exit_handler = CommandHandler("exit", exit_process)
    application.add_handler(exit_handler)
    logout_handler = CommandHandler("logout", logout)
    application.add_handler(logout_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("start_redact", start_redact))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("close", close))
    application.add_handler(CommandHandler("how_use_bot", how_use_bot))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("ekvalaizer", ekvalaizer))
    application.add_handler(CommandHandler("reverb", reverb))
    application.add_handler(CommandHandler("slow_fast", slow_fast))
    application.add_handler(CommandHandler("bass", bass))
    application.add_handler(CommandHandler("vocal_and_music", vocal_and_music))
    application.add_handler(CommandHandler("effect", effect))
    application.add_handler(CommandHandler("noise_delete", noise_delete))
    application.add_handler(CommandHandler("gross_beat", gross_beat))
    application.add_handler(CommandHandler("close_redact", close_redact))
    application.run_polling()


if __name__ == '__main__':
    main()
