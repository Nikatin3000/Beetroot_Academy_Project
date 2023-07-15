from telegram.ext import CommandHandler, ApplicationBuilder
import requests
import json

# Замените 'YOUR_BOT_TOKEN' на токен вашего телеграм-бота
bot_token = '6282355630:AAGBE9_VcDn5QUHYxUFJPgl5wA58LBMDpro'
# Замените 'http://your-domain.com/' на адрес вашего Django-приложения
api_url = 'http://127.0.0.1:8000/'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я твой книжный бот! Я могу помочь тебе найти книги и отметить их как прочитанные.")

def search_books(update, context):
    tags = context.args
    if tags:
        url = api_url + 'search-books/'
        data = {'tags': tags}
        response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        results = response.json()

        if 'results' in results:
            message = "Результаты поиска:\n"
            for book in results['results']:
                message += f"Название: {book['title']}, Автор: {book['author']}\n"
        else:
            message = "Книги с такими тегами не найдены."
    else:
        message = "Пожалуйста, укажите теги книг для поиска."

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def mark_as_read(update, context):
    if len(context.args) >= 2:
        book_id = context.args[0]
        user_id = context.args[1]

        url = api_url + 'mark-as-read/'
        data = {'book_id': book_id, 'user_id': user_id}
        response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        result = response.json()

        if 'status' in result and result['status'] == 'success':
            message = "Книга отмечена как прочитанная."
        else:
            message = "Не удалось отметить книгу как прочитанную."
    else:
        message = "Пожалуйста, укажите идентификатор книги и идентификатор пользователя."

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)



if __name__ == '__main__':
    updater = ApplicationBuilder().token(token=bot_token).build()

    start_handler = CommandHandler('start', start)
    search_books_handler = CommandHandler('search', search_books)
    mark_as_read_handler = CommandHandler('markread', mark_as_read)

    updater.add_handler(start_handler)
    updater.add_handler(search_books_handler)
    updater.add_handler(mark_as_read_handler)

    updater.run_polling()