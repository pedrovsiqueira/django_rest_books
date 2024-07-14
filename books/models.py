from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=100)
    published_date = models.DateField(auto_now_add=True)
    isbn_number = models.CharField(max_length=13)

    def __str__(self):
        return self.title
