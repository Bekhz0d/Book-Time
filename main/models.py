from typing import Any
from django.db import models
from readers.models import Readers
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    isbn = models.CharField(max_length=17)
    picture = models.ImageField(default='book-pictures/default_book_picture.png')
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    bio = models.TextField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    
class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.book.title} by {self.author.first_name} {self.author.last_name}'
    

class BookReview(models.Model):
    reader = models.ForeignKey(Readers, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField()
    stars_given = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
        )
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.stars_given} by {self.user.username}'
    
    
class ReaderRead(models.Model):
    reader = models.ForeignKey(Readers, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.reader.username} read {self.book.title}"
    

class ReaderReading(models.Model):
    reader = models.ForeignKey(Readers, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.reader.username} reading {self.book.title}"


class ReaderWillRead(models.Model):
    reader = models.ForeignKey(Readers, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.reader.username} wants to read {self.book.title}"
    

class ReaderRecommend(models.Model):
    reader = models.ForeignKey(Readers, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.reader.username} recommend {self.book.title}"
