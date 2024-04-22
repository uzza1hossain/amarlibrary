from django.db import models

# Create your models here.
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower


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
