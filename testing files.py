import os

from telegram.ext import Updater, CommandHandler, MessageHandler

from bass import bass_boost

TOKEN = '6750008375:AAFi-BbY5KNgSsQ1gfZG_BUA77mcgmCzgqw'


def start(update, context):
    update.message.reply_text('Привет! Отправь мне файл и число, и я усилю бас в твоем аудио.')


def handle_document(update, context):
    document = update.message.document
    file_id = document.file_id
    new_file = context.bot.get_file(file_id)
    file_path = f'{document.file_name}'
    new_file.download(file_path)
    update.message.reply_text('Файл получен. Теперь отправь мне число для усиления баса.')
    context.user_data['file_path'] = file_path


def handle_number(update, context):
    if 'file_path' not in context.user_data:
        update.message.reply_text('Сначала отправь файл.')
        return

    try:
        boost_value = int(update.message.text)
    except ValueError:
        update.message.reply_text('Пожалуйста, отправь число.')
        return

    file_path = context.user_data['file_path']
    processed_file_path = bass_boost(file_path, boost_value)

    with open(processed_file_path, 'rb') as audio_file:
        update.message.reply_audio(audio=audio_file, timeout=120)

    os.remove(file_path)


def main():
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document, handle_document))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_number))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
