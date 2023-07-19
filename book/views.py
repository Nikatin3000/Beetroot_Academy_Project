from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Book  #, ReadBook
from django.utils import timezone

def book_list(request):
    books = Book.objects.all()
    book_data = []
    for book in books:
        book_data.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'date_marked': book.date_marked
        })
    return JsonResponse({'books': book_data})

@csrf_exempt
def search_books(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tags = data['tags']

        books = Book.objects.filter(tags__name__in=tags).distinct()

        results = []
        for book in books:
            results.append({
                'title': book.title,
                'author': book.author,
            })

        return JsonResponse({'results': results})

@csrf_exempt
def mark_as_read(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        book_id = data['book_id']
        # user_id= data['user']

        try:
            book = Book.objects.get(pk=book_id)

            if not book.date_marked:  # Проверка наличия даты отметки
                book.date_marked = timezone.now()  # Запишите текущую дату и время, если поле пустое
                book.save()

                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'already_marked'})  # Книга уже была отмечена ранее

        except Book.DoesNotExist:
            return JsonResponse({'status': 'book_not_found'})

    return JsonResponse({'status': 'error'})

