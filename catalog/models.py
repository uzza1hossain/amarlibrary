from django.db import models
from django.conf import settings
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.utils import timezone
from datetime import timedelta

# Create your models here.


class Genre(models.Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction)."""

    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre (e.g. Science Fiction, Thriller etc.)",
    )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower("name"),
                name="genre_name_case_insensitive_unique",
                violation_error_message="Genre already exists (case insensitive match)",
            ),
        ]


class Book(models.Model):
    BORROW_STATUS_CHOICES = [
        ("on_loan", "On loan"),
        ("available", "Available"),
        ("reserved", "Reserved"),
    ]
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        "Author", on_delete=models.RESTRICT, related_name="books"
    )
    summary = models.TextField(blank=True, null=True, max_length=1000)
    personal_review = models.TextField(blank=True, null=True, max_length=1000)
    personal_rating = models.IntegerField(blank=True, null=True)
    isbn = models.CharField("ISBN", max_length=13, unique=True)
    genre = models.ManyToManyField(
        Genre, help_text="Select a genre for this book", related_name="books"
    )
    publication = models.ForeignKey(
        "Publication", on_delete=models.RESTRICT, related_name="books"
    )
    cover_image = models.ImageField(upload_to="covers/", blank=True, null=True)
    borrow_status = models.CharField(
        max_length=10,
        choices=BORROW_STATUS_CHOICES,
        default="available",
    )
    language = models.ForeignKey(
        "Language", on_delete=models.RESTRICT, related_name="books"
    )


class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrows")
    borrower = models.CharField(max_length=200)
    borrowed_date = models.DateField(auto_now_add=True)
    due_date = models.DateTimeField(default=timezone.now() + timedelta(days=15))
    returned_date = models.DateField(blank=True, null=True)
    returned = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)  # Call the "real" save() method.
    #     self.book.borrow_status = (
    #         "on_loan" if self.returned_date is None else "available"
    #     )
    #     self.book.save()
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        self.book.borrow_status = "available" if self.returned else "on_loan"
        self.book.save()


class Note(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="notes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]


class Author(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    is_public = models.BooleanField(default=True)


class Publication(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True, max_length=1000)
    is_public = models.BooleanField(default=True)


class Language(models.Model):
    name = models.CharField(max_length=200)
