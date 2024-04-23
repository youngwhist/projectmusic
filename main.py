import os
import sqlite3

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackContext

from bass import bass_boost
from effects import effectss
from fast_or_slow import slowfast_music
from grossbit import gross_bit
from nonoise import remove_noise
from obrez import obrezkaa
from razdel_voice import split_audioo
from reverb import reverbb
from reverse import reverse_audio_filee


def chisl(s):
    return all(char.isdigit() or char == '.' for char in s)


BOT_TOKEN = "6760985613:AAEYf8uj5RWPXQiGQRhs2j3YjFpUbhBhOck"
# ссылка на бота https://t.me/forsoul_music_bot


# Состояния
REGISTER, LOGIN, WAITING_FOR_AUDIO, WAITING_FOR_INT_VALUE, = range(4)

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
    await update.message.reply_text("Что бы воспользоваться функционалам, перейдите в /start_redact. Выберите метод редактирования который вам нужен, после чего вызовите функцию через клавиатуру которая внизу экрана. После этого делайте то что вам скажет бот. После редактирования файла он скинет вам итоговый результат и вы можете его скачать.")


async def about(update: Update, context: CallbackContext):
    await update.message.reply_text("Проект представляет бесплатный ресурс по редактированию звуковых файлов и дальшейшим их сохранением. Над проектом работали Стрельников Михаил, Горский Владислав, Кузнецов Владимир. Проект опенсурс и вы можете ознакомиться с ним на github https://github.com/youngwhist/projectmusic/. Так же проект размещён на сайте и вы можете использовать его вместо бота.")


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

# Блок кода с вызовом функций
# --------------------------------------------------------------------------------------------------------------------

async def start_redact(update, context):
    redact_markup = ReplyKeyboardMarkup([
        ['/reverse', '/reverb', '/slow_fast'],
        ['/effect', '/noise_delete', '/gross_beat'],
        ['/bass', '/vocal_and_music', '/obrezka'],
        ['/close']
    ], one_time_keyboard=False)
    await update.message.reply_text("ВНИМАНИЕ! НЕ пытайтесь вызвать другие команды пока находитесь в моменте выполнения одной. Это обернётся ошибкой. Что бы выйти из функции в момент выполнения введите команду /cancel_funct")

    await update.message.reply_text(
        "Выберите опцию для редактирования:",
        reply_markup=redact_markup
    )


async def reverse(update, context):
    await update.message.reply_text(
        "Привет! Пришли мне звуковой файл. Что бы выйти из команды введи /cancel_funct"
    )
    return WAITING_FOR_AUDIO


async def reverb(update, context):
    await update.message.reply_text(
        "Привет! Пришли мне звуковой файл. Что бы выйти из команды введи /cancel_funct"
    )
    return WAITING_FOR_AUDIO


async def slow_fast(update, context):
    await update.message.reply_text(
        "Привет! Пришли мне звуковой файл. Что бы выйти из команды введи /cancel_funct"
    )
    return WAITING_FOR_AUDIO


async def bass(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Привет! Пришли мне звуковой файл. Что бы выйти из команды введи /cancel_funct"
    )
    return WAITING_FOR_AUDIO


async def vocal_and_music(update, context):
    await update.message.reply_text(
        "Привет! Пришли мне звуковой файл. Что бы выйти из команды введи /cancel_funct"
    )
    return WAITING_FOR_AUDIO


async def effect(update, context):
    await update.message.reply_text(
        "Привет! Пришли мне звуковой файл. Что бы выйти из команды введи /cancel_funct"
    )
    return WAITING_FOR_AUDIO


async def obrezka(update, context):
    await update.message.reply_text(
        "Привет! Пришли мне звуковой файл. Что бы выйти из команды введи /cancel_funct"
    )
    return WAITING_FOR_AUDIO


async def noise_delete(update, context):
    await update.message.reply_text(
        "Привет! Пришли мне звуковой файл. Что бы выйти из команды введи /cancel_funct"
    )
    return WAITING_FOR_AUDIO


async def gross_beat(update, context):
    await update.message.reply_text(
        "Привет! Пришли мне звуковой файл. Что бы выйти из команды введи /cancel_funct"
    )
    return WAITING_FOR_AUDIO


async def close_redact(update, context):
    await update.message.reply_text(
        "Выберите опцию:",
        reply_markup=main_menu_markup
    )


async def cancel_funct(update: Update, context: CallbackContext):
    await update.message.reply_text('Функция прервана. ')
    return ConversationHandler.END


# Конец блока кода
# --------------------------------------------------------------------------------------------------------------------

# Блок кода с обработкой функций
# --------------------------------------------------------------------------------------------------------------------

async def handle_audio_fastslow(update: Update, context: CallbackContext) -> int:
    audio_file = update.message.audio or update.message.document
    if audio_file:
        file_extension = os.path.splitext(audio_file.file_name)[1].lower()
        if file_extension in ['.wav', '.mp3', '.ogg', '.flac', '.m4a']:
            file_id = audio_file.file_id
            new_file = await context.bot.get_file(file_id)
            local_file_path = await new_file.download_to_drive(f'audio{file_extension}')
            context.user_data['audio_file_path'] = local_file_path
            await update.message.reply_text(
                "Спасибо! Теперь введи целое число если хочешь ускорить трек, а если замедлить то нецелое число.")
            return WAITING_FOR_INT_VALUE
        else:
            await update.message.reply_text(
                "Пожалуйста, пришли звуковой файл в поддерживаемом формате (WAV, MP3, OGG, FLAC, M4A).")
            return WAITING_FOR_AUDIO
    else:
        await update.message.reply_text("Пожалуйста, пришли звуковой файл.")
        return WAITING_FOR_AUDIO


async def handle_int_value_fastslow(update: Update, context: CallbackContext) -> int:
    int_value = update.message.text
    if int_value:
        if chisl(int_value):
            int_value = float(int_value)
            local_file_path = str(context.user_data.get('audio_file_path'))
            if local_file_path:
                with open(local_file_path, 'rb') as audio_file:
                    slowfast_music(local_file_path, int_value)
                    await update.message.reply_audio(audio=audio_file)

                os.remove(local_file_path)
            else:
                await update.message.reply_text("Не удалось найти аудиофайл для отправки.")

            return ConversationHandler.END
        else:
            await update.message.reply_text("Введите число.")


async def handle_audio_bass(update: Update, context: CallbackContext) -> int:
    audio_file = update.message.audio or update.message.document
    if audio_file:
        file_extension = os.path.splitext(audio_file.file_name)[1].lower()
        if file_extension in ['.wav', '.mp3', '.ogg', '.flac', '.m4a']:
            file_id = audio_file.file_id
            new_file = await context.bot.get_file(file_id)
            local_file_path = await new_file.download_to_drive(f'audio{file_extension}')
            context.user_data['audio_file_path'] = local_file_path
            await update.message.reply_text("Спасибо! Теперь введи целое число.")
            return WAITING_FOR_INT_VALUE
        else:
            await update.message.reply_text(
                "Пожалуйста, пришли звуковой файл в поддерживаемом формате (WAV, MP3, OGG, FLAC, M4A).")
            return WAITING_FOR_AUDIO
    else:
        await update.message.reply_text("Пожалуйста, пришли звуковой файл.")
        return WAITING_FOR_AUDIO


async def handle_int_value_bass(update: Update, context: CallbackContext) -> int:
    int_value = update.message.text
    if int_value:
        if chisl(int_value):
            int_value = float(int_value)
            local_file_path = context.user_data.get('audio_file_path')
            if local_file_path:
                with open(local_file_path, 'rb') as audio_file:
                    bass_boost(local_file_path, local_file_path, int_value)
                    await update.message.reply_audio(audio=audio_file)

                os.remove(local_file_path)
            else:
                await update.message.reply_text("Не удалось найти аудиофайл для отправки.")

            return ConversationHandler.END

    else:
        await update.message.reply_text("Введите целое число.")


async def handle_audio_grossbeat(update: Update, context: CallbackContext) -> int:
    audio_file = update.message.audio or update.message.document
    if audio_file:
        file_extension = os.path.splitext(audio_file.file_name)[1].lower()
        if file_extension in ['.wav', '.mp3', '.ogg', '.flac', '.m4a']:
            file_id = audio_file.file_id
            new_file = await context.bot.get_file(file_id)
            local_file_path = await new_file.download_to_drive(f'audio{file_extension}')
            context.user_data['audio_file_path'] = local_file_path
            await update.message.reply_text("Спасибо! Теперь введи целое число.")
            return WAITING_FOR_INT_VALUE
        else:
            await update.message.reply_text(
                "Пожалуйста, пришли звуковой файл в поддерживаемом формате (WAV, MP3, OGG, FLAC, M4A).")
            return WAITING_FOR_AUDIO
    else:
        await update.message.reply_text("Пожалуйста, пришли звуковой файл.")
        return WAITING_FOR_AUDIO


async def handle_int_value_grossbeat(update: Update, context: CallbackContext) -> int:
    int_value = update.message.text
    if int_value:
        if chisl(int_value):
            int_value = float(update.message.text)
            local_file_path = str(context.user_data.get('audio_file_path'))
            if local_file_path:
                with open(local_file_path, 'rb') as audio_file:
                    gross_bit(local_file_path, int_value)
                    await update.message.reply_audio(audio=audio_file)

                os.remove(local_file_path)
            else:
                await update.message.reply_text("Не удалось найти аудиофайл для отправки.")

            return ConversationHandler.END
        else:
            await update.message.reply_text("Введите целое число.")


async def handle_audio_nonoise(update: Update, context: CallbackContext) -> int:
    audio_file = update.message.audio or update.message.document
    if audio_file:
        file_extension = os.path.splitext(audio_file.file_name)[1].lower()
        if file_extension in ['.wav', '.mp3', '.ogg', '.flac', '.m4a']:
            file_id = audio_file.file_id
            new_file = await context.bot.get_file(file_id)
            local_file_path = await new_file.download_to_drive(f'audio{file_extension}')
            context.user_data['audio_file_path'] = local_file_path
            await update.message.reply_text("Спасибо! Теперь введи целое число.")
            return WAITING_FOR_INT_VALUE
        else:
            await update.message.reply_text(
                "Пожалуйста, пришли звуковой файл в поддерживаемом формате (WAV, MP3, OGG, FLAC, M4A).")
            return WAITING_FOR_AUDIO
    else:
        await update.message.reply_text("Пожалуйста, пришли звуковой файл.")
        return WAITING_FOR_AUDIO


async def handle_int_value_nonoise(update: Update, context: CallbackContext) -> int:
    int_value = update.message.text
    if int_value:
        if chisl(int_value):
            int_value = float(update.message.text)
            local_file_path = str(context.user_data.get('audio_file_path'))
            if local_file_path:
                with open(local_file_path, 'rb') as audio_file:
                    remove_noise(local_file_path, int_value)
                    await update.message.reply_audio(audio=audio_file)

                os.remove(local_file_path)
            else:
                await update.message.reply_text("Не удалось найти аудиофайл для отправки.")

            return ConversationHandler.END
        else:
            await update.message.reply_text("Введите целое число.")


async def handle_audio_obrez(update: Update, context: CallbackContext) -> int:
    audio_file = update.message.audio or update.message.document
    if audio_file:
        file_extension = os.path.splitext(audio_file.file_name)[1].lower()
        if file_extension in ['.wav', '.mp3', '.ogg', '.flac', '.m4a']:
            file_id = audio_file.file_id
            new_file = await context.bot.get_file(file_id)
            local_file_path = await new_file.download_to_drive(f'audio{file_extension}')
            context.user_data['audio_file_path'] = local_file_path
            await update.message.reply_text(
                "Спасибо! Теперь введите 2 целых числа, первое - начало обрезания второе конец.")
            return WAITING_FOR_INT_VALUE
        else:
            await update.message.reply_text(
                "Пожалуйста, пришли звуковой файл в поддерживаемом формате (WAV, MP3, OGG, FLAC, M4A).")
            return WAITING_FOR_AUDIO
    else:
        await update.message.reply_text("Пожалуйста, пришли звуковой файл.")
        return WAITING_FOR_AUDIO


async def handle_int_value_obrez(update: Update, context: CallbackContext) -> int:
    int_value = update.message.text
    parts = int_value.split()
    if len(parts) == 2:

        param1, param2 = parts
        param1 = float(param1)
        param2 = float(param2)

        local_file_path = str(context.user_data.get('audio_file_path'))

        if local_file_path:
            with open(local_file_path, 'rb') as audio_file:
                obrezkaa(local_file_path, local_file_path, param1, param2)
                await update.message.reply_audio(audio=audio_file)

            os.remove(local_file_path)
        else:
            await update.message.reply_text("Не удалось найти аудиофайл для отправки.")

        return ConversationHandler.END
    else:
        await update.message.reply_text("Введите 2 целых числа.")


async def handle_audio_reverse(update: Update, context: CallbackContext) -> int:
    audio_file = update.message.audio or update.message.document
    if audio_file:
        file_extension = os.path.splitext(audio_file.file_name)[1].lower()
        if file_extension in ['.wav', '.mp3', '.ogg', '.flac', '.m4a']:  # Добавьте другие расширения, если нужно
            file_id = audio_file.file_id
            new_file = await context.bot.get_file(file_id)
            local_file_path = await new_file.download_to_drive(f'audio{file_extension}')
            context.user_data['audio_file_path'] = local_file_path
            with open(local_file_path, 'rb') as audio_file:
                reverse_audio_filee(local_file_path, local_file_path)
                await update.message.reply_audio(audio=audio_file)

            os.remove(local_file_path)

            return ConversationHandler.END

        else:
            await update.message.reply_text(
                "Пожалуйста, пришли звуковой файл в поддерживаемом формате (WAV, MP3, OGG, FLAC, M4A).")
            return WAITING_FOR_AUDIO
    else:
        await update.message.reply_text("Пожалуйста, пришли звуковой файл.")
        return WAITING_FOR_AUDIO


async def handle_audio_reverb(update: Update, context: CallbackContext) -> int:
    audio_file = update.message.audio or update.message.document
    if audio_file:
        file_extension = os.path.splitext(audio_file.file_name)[1].lower()
        if file_extension in ['.wav', '.mp3', '.ogg', '.flac', '.m4a']:
            file_id = audio_file.file_id
            new_file = await context.bot.get_file(file_id)
            local_file_path = await new_file.download_to_drive(f'audio{file_extension}')
            context.user_data['audio_file_path'] = local_file_path
            await update.message.reply_text("Спасибо! Теперь введите 2 целых числа.")
            return WAITING_FOR_INT_VALUE
        else:
            await update.message.reply_text(
                "Пожалуйста, пришли звуковой файл в поддерживаемом формате (WAV, MP3, OGG, FLAC, M4A).")
            return WAITING_FOR_AUDIO
    else:
        await update.message.reply_text("Пожалуйста, пришли звуковой файл.")
        return WAITING_FOR_AUDIO


# Функция для обработки целочисленных значений
async def handle_int_value_reverb(update: Update, context: CallbackContext) -> int:
    int_value = update.message.text
    parts = int_value.split()
    if len(parts) == 2:

        param1, param2 = parts
        param1 = float(param1)
        param2 = float(param2)

        local_file_path = str(context.user_data.get('audio_file_path'))

        if local_file_path:
            with open(local_file_path, 'rb') as audio_file:
                reverbb(local_file_path, local_file_path, param1, param2)
                await update.message.reply_audio(audio=audio_file)

            os.remove(local_file_path)
        else:
            await update.message.reply_text("Не удалось найти аудиофайл для отправки.")

        return ConversationHandler.END

    else:
        await update.message.reply_text("Введите 2 целых числа.")


async def handle_audio_vocal_and_music(update: Update, context: CallbackContext) -> int:
    audio_file = update.message.audio or update.message.document
    if audio_file:
        file_extension = os.path.splitext(audio_file.file_name)[1].lower()
        if file_extension in ['.wav', '.mp3', '.ogg', '.flac', '.m4a']:
            file_id = audio_file.file_id
            new_file = await context.bot.get_file(file_id)
            local_file_path = await new_file.download_to_drive(f'audio{file_extension}')
            context.user_data['audio_file_path'] = local_file_path
            await update.message.reply_text("Спасибо! Теперь введи целое число.")
            return WAITING_FOR_INT_VALUE
        else:
            await update.message.reply_text(
                "Пожалуйста, пришли звуковой файл в поддерживаемом формате (WAV, MP3, OGG, FLAC, M4A).")
            return WAITING_FOR_AUDIO
    else:
        await update.message.reply_text("Пожалуйста, пришли звуковой файл.")
        return WAITING_FOR_AUDIO


async def handle_int_value_vocal_and_music(update: Update, context: CallbackContext) -> int:
    int_value = update.message.text
    if int_value:
        if chisl(int_value):
            int_value = int(update.message.text)
            local_file_path = str(context.user_data.get('audio_file_path'))
            voice = 'voice_audio.waw'
            music = 'music_auido.waw'
            if local_file_path:
                with open(local_file_path, 'rb') as audio_file:
                    split_audioo(local_file_path, voice, music, int_value)

                await update.message.reply_audio(audio=voice)
                await update.message.reply_audio(audio=music)

                os.remove(local_file_path)
                os.remove(voice)
                os.remove(music)
            else:
                await update.message.reply_text("Не удалось найти аудиофайл для отправки.")
            return ConversationHandler.END
    else:
        await update.message.reply_text("Введите целое число.")


async def handle_audio_effects(update: Update, context: CallbackContext) -> int:
    context.user_data['blocked'] = True
    audio_file = update.message.audio or update.message.document
    if audio_file:
        file_extension = os.path.splitext(audio_file.file_name)[1].lower()
        if file_extension in ['.wav', '.mp3', '.ogg', '.flac', '.m4a']:  # Добавьте другие расширения, если нужно
            file_id = audio_file.file_id
            new_file = await context.bot.get_file(file_id)
            local_file_path = await new_file.download_to_drive(f'audio{file_extension}')
            context.user_data['audio_file_path'] = local_file_path
            await update.message.reply_text("Спасибо! Теперь введите 5 целых чисел.")

            return WAITING_FOR_INT_VALUE
        else:
            await update.message.reply_text(
                "Пожалуйста, пришли звуковой файл в поддерживаемом формате (WAV, MP3, OGG, FLAC, M4A).")
            return WAITING_FOR_AUDIO
    else:
        await update.message.reply_text("Пожалуйста, пришли звуковой файл.")
        return WAITING_FOR_AUDIO


async def handle_int_value_effects(update: Update, context: CallbackContext) -> int:
    int_value = update.message.text
    parts = int_value.split()

    if len(parts) == 5:

        param1, param2, param3, param4, param5 = parts
        param1 = float(param1)
        param2 = float(param2)
        param3 = float(param3)
        param4 = float(param4)
        param5 = float(param5)
        local_file_path = str(context.user_data.get('audio_file_path'))
        if local_file_path:
            with open(local_file_path, 'rb') as audio_file:
                effectss(local_file_path, param1, param2, param3, param4, param5)
                await update.message.reply_audio(audio=audio_file)

            os.remove(local_file_path)
        else:
            await update.message.reply_text("Не удалось найти аудиофайл для отправки.")

        return ConversationHandler.END
    else:
        await update.message.reply_text("Введите 5 целых чисел.")



# Конец блока кода
# --------------------------------------------------------------------------------------------------------------------

# Блок кода с запуском бота
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

    # Прочие обработчики для функций
    conv_handler_bass = ConversationHandler(
        entry_points=[CommandHandler('bass', bass)],
        states={
            WAITING_FOR_AUDIO: [MessageHandler(filters.Document.ALL, handle_audio_bass)],
            WAITING_FOR_INT_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_int_value_bass)]
        },
        fallbacks=[CommandHandler('cancel_funct', cancel_funct)]
    )

    conv_handler_slow_fast = ConversationHandler(
        entry_points=[CommandHandler('slow_fast', slow_fast)],
        states={
            WAITING_FOR_AUDIO: [MessageHandler(filters.Document.ALL, handle_audio_fastslow)],
            WAITING_FOR_INT_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_int_value_fastslow)]
        },
        fallbacks=[CommandHandler('cancel_funct', cancel_funct)]
    )

    conv_handler_grossbit = ConversationHandler(
        entry_points=[CommandHandler('gross_beat', gross_beat)],
        states={
            WAITING_FOR_AUDIO: [MessageHandler(filters.Document.ALL, handle_audio_grossbeat)],
            WAITING_FOR_INT_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_int_value_grossbeat)]
        },
        fallbacks=[CommandHandler('cancel_funct', cancel_funct)]
    )

    conv_handler_nonoise = ConversationHandler(
        entry_points=[CommandHandler('noise_delete', noise_delete)],
        states={
            WAITING_FOR_AUDIO: [MessageHandler(filters.Document.ALL, handle_audio_nonoise)],
            WAITING_FOR_INT_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_int_value_nonoise)]
        },
        fallbacks=[CommandHandler('cancel_funct', cancel_funct)]
    )

    conv_handler_obrez = ConversationHandler(
        entry_points=[CommandHandler('obrezka', obrezka)],
        states={
            WAITING_FOR_AUDIO: [MessageHandler(filters.Document.ALL, handle_audio_obrez)],
            WAITING_FOR_INT_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_int_value_obrez)]
        },
        fallbacks=[CommandHandler('cancel_funct', cancel_funct)]
    )

    conv_handler_reverse = ConversationHandler(
        entry_points=[CommandHandler('reverse', reverse)],
        states={
            WAITING_FOR_AUDIO: [MessageHandler(filters.Document.ALL, handle_audio_reverse)],
        },
        fallbacks=[CommandHandler('cancel_funct', cancel_funct)]
    )

    conv_handler_reverb = ConversationHandler(
        entry_points=[CommandHandler('reverb', reverb)],
        states={
            WAITING_FOR_AUDIO: [MessageHandler(filters.Document.ALL, handle_audio_reverb)],
            WAITING_FOR_INT_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_int_value_reverb)]
        },
        fallbacks=[CommandHandler('cancel_funct', cancel_funct)]
    )

    conv_handler_vocal_and_music = ConversationHandler(
        entry_points=[CommandHandler('vocal_and_music', vocal_and_music)],
        states={
            WAITING_FOR_AUDIO: [MessageHandler(filters.Document.ALL, handle_audio_vocal_and_music)],
            WAITING_FOR_INT_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_int_value_vocal_and_music)]
        },
        fallbacks=[CommandHandler('cancel_funct', cancel_funct)]
    )

    conv_handler_effects = ConversationHandler(
        entry_points=[CommandHandler('effect', effect)],
        states={
            WAITING_FOR_AUDIO: [MessageHandler(filters.Document.ALL, handle_audio_effects)],
            WAITING_FOR_INT_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_int_value_effects)]
        },
        fallbacks=[CommandHandler('cancel_funct', cancel_funct)]
    )

    # Обработчики и запуск кода
    application.add_handler(register_handler)
    application.add_handler(login_handler)
    application.add_handler(conv_handler_bass)
    application.add_handler(conv_handler_slow_fast)
    application.add_handler(conv_handler_grossbit)
    application.add_handler(conv_handler_nonoise)
    application.add_handler(conv_handler_obrez)
    application.add_handler(conv_handler_reverse)
    application.add_handler(conv_handler_reverb)
    application.add_handler(conv_handler_vocal_and_music)
    application.add_handler(conv_handler_effects)
    exit_handler = CommandHandler("exit", exit_process)
    application.add_handler(exit_handler)
    logout_handler = CommandHandler("logout", logout)
    application.add_handler(logout_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("start_redact", start_redact))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("close", close))
    application.add_handler(CommandHandler("cancel_funct", cancel_funct))
    application.add_handler(CommandHandler("how_use_bot", how_use_bot))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("reverse", reverse))
    application.add_handler(CommandHandler("reverb", reverb))
    application.add_handler(CommandHandler("slow_fast", slow_fast))
    application.add_handler(CommandHandler("bass", bass))
    application.add_handler(CommandHandler("vocal_and_music", vocal_and_music))
    application.add_handler(CommandHandler("effect", effect))
    application.add_handler(CommandHandler("obrezka", obrezka))
    application.add_handler(CommandHandler("noise_delete", noise_delete))
    application.add_handler(CommandHandler("gross_beat", gross_beat))
    application.add_handler(CommandHandler("close_redact", close_redact))
    application.run_polling()


if __name__ == '__main__':
    main()
