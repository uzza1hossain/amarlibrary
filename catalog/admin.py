from django.contrib import admin

from .models import Genre, Book, Borrow, Author, Publication, Note, Language

# Register your models here.

admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Borrow)
admin.site.register(Author)
admin.site.register(Publication)
admin.site.register(Note)
admin.site.register(Language)
