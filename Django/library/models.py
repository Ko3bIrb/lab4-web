from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class Author(models.Model):
    first_name = models.CharField("Имя", max_length=80)
    last_name = models.CharField("Фамилия", max_length=80)
    # Пустой текст хранится как пустая строка, без отдельного значения NULL.
    biography = models.TextField("Биография", blank=True, default="")
    photo = models.ImageField("Фото", upload_to="authors/", blank=True)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ("last_name", "first_name")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField("Название", max_length=200)
    publication_year = models.PositiveSmallIntegerField(
        "Год издания",
        validators=[MinValueValidator(1), MaxValueValidator(9999)],
    )
    isbn = models.CharField(
        "ISBN",
        max_length=13,
        unique=True,
        validators=[
            RegexValidator(
                r"^(?:[0-9]{9}[0-9X]|[0-9]{13})\Z",
                "Введите ISBN из 10 или 13 символов без дефисов и пробелов.",
            ),
        ],
    )
    # Один автор может иметь много книг. После его удаления Django удалит
    # связанные книги. Обратный доступ к ним доступен через author.books.
    # null и blank запрещают пропуск автора в БД и форме соответственно.
    # Значение по умолчанию отсутствует: автора выбирают явно.
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",
        verbose_name="Автор",
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ("title",)

    def __str__(self):
        return self.title
