# Generated by Django 5.0.4 on 2024-04-23 15:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_author_language_publication_book_borrow_note"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="isbn",
            field=models.CharField(
                blank=True, max_length=13, null=True, unique=True, verbose_name="ISBN"
            ),
        ),
        migrations.AlterField(
            model_name="borrow",
            name="due_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 5, 8, 15, 11, 7, 264420, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]