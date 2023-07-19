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
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я твой книжный бот! Я могу помочь тебе найти книги и отметить их как прочитанные.")

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
                            book_info = f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}"
                            if book['date_marked']:
                                date_marked = datetime.datetime.strptime(book['date_marked'], '%Y-%m-%dT%H:%M:%S.%fZ')
                                book_info += f", Дата прочтения: {date_marked.strftime('%d.%m.%Y %H:%M')}"
                            message += book_info + "\n"

                    else:
                        message = "Книги не найдены."
                else:
                    message = "Произошла ошибка при получении списка книг. Пожалуйста, попробуйте еще раз позже."

                await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        except Exception as e:
            logging.error(f"Ошибка при получении списка книг: {e}")
            message = "Произошла ошибка при получении списка книг. Пожалуйста, попробуйте еще раз позже."
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)



async def search_books(update: Update, context: CallbackContext) -> None:
    tags = context.args
    if not tags:
        message = "Пожалуйста, укажите теги книг для поиска."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        return

    url = api_url + 'search-books/'
    data = {'tags': tags}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'}) as response:
                results = await response.json()

            if 'results' in results:
                message = "Результаты поиска:\n"
                for book in results['results']:
                    book_info = f"Название: {book['title']}, Автор: {book['author']}"

                    if 'url' in book:
                        book_url = book['url']
                        book_info += f"\nURL: {book_url}"

                    message += "\n" + book_info

            else:
                message = "Книги с такими тегами не найдены."

            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        except Exception as e:
            logging.error(f"Ошибка при выполнении запроса поиска книг: {e}")
            message = "Произошла ошибка при выполнении запроса поиска книг. Пожалуйста, попробуйте еще раз позже."
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
async def mark_as_read(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 1:
        message = "Пожалуйста, укажите идентификатор книги."
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
                message = f"Книга отмечена как прочитанная. Дата и время отметки: {current_datetime}"
            else:
                message = "Не удалось отметить книгу как прочитанную."

            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        except Exception as e:
            logging.error(f"Ошибка при отметке книги как прочитанной: {e}")
            message = "Произошла ошибка при отметке книги как прочитанной. Пожалуйста, попробуйте еще раз позже."
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
