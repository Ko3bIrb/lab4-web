from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Author, Book


class AuthorBookTests(TestCase):
    def test_reverse_relation_and_cascade(self):
        author = Author.objects.create(first_name="Анна", last_name="Волкова")
        other = Author.objects.create(first_name="Олег", last_name="Смирнов")
        for title, isbn in [("Книга 1", "9785600000011"), ("Книга 2", "9785600000028")]:
            author.books.create(title=title, publication_year=2024, isbn=isbn)
        remaining = other.books.create(
            title="Другая книга", publication_year=2024, isbn="9785600000035"
        )
        self.assertEqual(author.books.count(), 2)

        author.delete()

        self.assertEqual(list(Book.objects.values_list("pk", flat=True)), [remaining.pk])

    def test_author_is_required(self):
        book = Book(title="Черновик", publication_year=2024, isbn="9785600000011")
        with self.assertRaises(ValidationError) as error:
            book.full_clean()
        self.assertIn("author", error.exception.message_dict)


class CatalogTests(TestCase):
    def test_catalog_shows_books_and_related_authors(self):
        author = Author.objects.create(first_name="Анна", last_name="Волкова")
        author.books.create(title="Город у реки", publication_year=2022, isbn="9785600000018")

        response = self.client.get(reverse("library:index"))

        self.assertTemplateUsed(response, "library/index.html")
        for value in ("Город у реки", "Анна Волкова", "2022", "9785600000018"):
            self.assertContains(response, value)

    def test_catalog_shows_empty_state(self):
        response = self.client.get(reverse("library:index"))

        self.assertContains(response, "В каталоге пока нет книг.")
