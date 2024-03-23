from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler

BOT_TOKEN = "6760985613:AAEYf8uj5RWPXQiGQRhs2j3YjFpUbhBhOck"
# ссылка на бота https://t.me/forsoul_music_bot
help_markup = ReplyKeyboardMarkup([['/how_use_bot', '/about'], ['/close']], one_time_keyboard=False)
main_menu_markup = ReplyKeyboardMarkup([['/start_redact', '/help'], ['/start']], one_time_keyboard=False)


async def help(update, context):
    await update.message.reply_text(
        "Узнать как пользоваться ботом: /how_use_bot. Узнать о проекте: /about. Выйти: /close",
        reply_markup=help_markup
    )


async def how_use_bot(update, context):
    await update.message.reply_text("Тут текст как юзать бота")


async def about(update, context):
    await update.message.reply_text("Тут текст о проекте")


async def close(update, context):
    await update.message.reply_text(
        "Выберите опцию:",
        reply_markup=main_menu_markup
    )


async def start(update, context):
    await update.message.reply_text(
        "Привет! Чтобы пользоваться ботом, нужно авторизоваться! Если у тебя нет аккаунта, то зарегистрируйся!",
        reply_markup=main_menu_markup
    )


async def start_redact(update, context):
    redact_markup = ReplyKeyboardMarkup([
        ['/ekvalaizer', '/reverb', '/slow'],
        ['/fast', '/bass', '/vocal_and_music'],
        ['/effect', '/noise_delete', '/gross_beat'],
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


async def slow(update, context):
    await update.message.reply_text("Слоу")


async def fast(update, context):
    await update.message.reply_text("Фаст")


async def bass(update, context):
    await update.message.reply_text("Басс бдуст")


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


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("start_redact", start_redact))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("close", close))
    application.add_handler(CommandHandler("how_use_bot", how_use_bot))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("ekvalaizer", ekvalaizer))
    application.add_handler(CommandHandler("reverb", reverb))
    application.add_handler(CommandHandler("slow", slow))
    application.add_handler(CommandHandler("fast", fast))
    application.add_handler(CommandHandler("bass", bass))
    application.add_handler(CommandHandler("vocal_and_music", vocal_and_music))
    application.add_handler(CommandHandler("effect", effect))
    application.add_handler(CommandHandler("noise_delete", noise_delete))
    application.add_handler(CommandHandler("gross_beat", gross_beat))
    application.add_handler(CommandHandler("close_redact", close_redact))
    application.run_polling()


if __name__ == '__main__':
    main()
