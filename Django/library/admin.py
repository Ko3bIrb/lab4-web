from django.contrib import admin
from django.db.models import Count

from .models import Author, Book


class BookInline(admin.TabularInline):
    model = Book
    extra = 0
    show_change_link = True


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "books_count")
    search_fields = ("last_name", "first_name", "biography")
    inlines = (BookInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(book_total=Count("books"))

    @admin.display(description="Книг", ordering="book_total")
    def books_count(self, obj):
        return obj.book_total


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year", "isbn")
    list_filter = ("author", "publication_year")
    list_editable = ("publication_year",)
    search_fields = ("title", "isbn", "author__last_name")
    list_select_related = ("author",)


admin.site.site_header = "Библиотека"
admin.site.site_title = "Библиотека"
admin.site.index_title = "Управление каталогом"
