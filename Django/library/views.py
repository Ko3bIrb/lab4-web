from django.shortcuts import render

from .models import Book


def index(request):
    books = Book.objects.select_related("author")
    context = {"title": "Каталог библиотеки", "books": books}
    return render(request, "library/index.html", context)
