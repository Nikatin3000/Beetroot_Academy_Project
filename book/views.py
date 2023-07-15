from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Book, Tag, ReadBook

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
        user= data['user']

        book = Book.objects.get(pk=book_id)

        read_book = ReadBook(book=book, user_id=user)
        read_book.save()

        return JsonResponse({'status': 'success'})

