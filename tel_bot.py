from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes, CallbackContext
import json
from telegram import Update
import logging
import aiohttp
import datetime

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

bot_token = '6282355630:AAGBE9_VcDn5QUHYxUFJPgl5wA58LBMDpro'

api_url = 'http://127.0.0.1:8000/book/'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привіт, я твій книжковий бот! Я можу допомогти тобі знайти книжки та відмітити їх як прочитані.")

async def book_list(update: Update, context: CallbackContext) -> None:
    url = api_url + 'book_list/'

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers={'Accept': 'application/json'}) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'books' in data:
                        message = "Список книг:\n"
                        for book in data['books']:
                            book_info = f"ID: {book['id']}, Назва: {book['title']}, Автор: {book['author']}"
                            if book['date_marked']:
                                date_marked = datetime.datetime.strptime(book['date_marked'], '%Y-%m-%dT%H:%M:%S.%fZ')
                                book_info += f", Дата прочитання: {date_marked.strftime('%d.%m.%Y %H:%M')}"
                            message += book_info + "\n"

                    else:
                        message = "Книгу не знайдено."
                else:
                    message = "Сталася помилка під час отримання списку книг. Будь ласка, спробуйте ще раз пізніше."

                await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        except Exception as e:
            logging.error(f"Помилка під час отримання списку книг: {e}")
            message = "Сталася помилка під час отримання списку книг. Будь ласка, спробуйте ще раз пізніше."
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)



async def search_books(update: Update, context: CallbackContext) -> None:
    tags = context.args
    if not tags:
        message = "Будь ласка, вкажіть теги книг для пошуку."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        return

    url = api_url + 'search-books/'
    data = {'tags': tags}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'}) as response:
                results = await response.json()

            if 'results' in results:
                message = "Результат пошуку:\n"
                for book in results['results']:
                    book_info = f"Назва: {book['title']}, Автор: {book['author']}"

                    if 'url' in book:
                        book_url = book['url']
                        book_info += f"\nURL: {book_url}"

                    message += "\n" + book_info

            else:
                message = "Книжки з такими тегами не знайдено."

            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        except Exception as e:
            logging.error(f"Помилка під час виконання запиту пошуку книг: {e}")
            message = "Сталася помилка під час виконання запиту пошуку книг. Будь ласка, спробуйте ще раз пізніше."
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
async def mark_as_read(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 1:
        message = "Будь ласка, вкажіть ID книги."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        return

    book_id = context.args[0]
    url = api_url + 'mark-as-read/'

    # Получаем текущую дату и время
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    data = {'book_id': book_id, 'date_time': current_datetime}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'}) as response:
                result = await response.json()

            if 'status' in result and result['status'] == 'success':
                message = f"Книгу відмічено як прочитану. Дата і час відмітки: {current_datetime}"
            else:
                message = "Не вдалося відзначити книгу як прочитану."

            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        except Exception as e:
            logging.error(f"Помилка під час відмітки книги як прочитаної: {e}")
            message = "Сталася помилка під час позначення книги як прочитаної. Будь ласка, спробуйте ще раз пізніше."
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


if __name__ == '__main__':
    updater = ApplicationBuilder().token(token=bot_token).build()

    start_handler = CommandHandler('start', start)
    search_books_handler = CommandHandler('search', search_books)
    mark_as_read_handler = CommandHandler('markread', mark_as_read)
    book_list_handler = CommandHandler('booklist', book_list)

    updater.add_handler(start_handler)
    updater.add_handler(search_books_handler)
    updater.add_handler(mark_as_read_handler)
    updater.add_handler(book_list_handler)

    updater.run_polling()
