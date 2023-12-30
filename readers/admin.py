from django.contrib import admin
from main.models import Book, BookAuthor, BookReview, ReaderRead, \
    ReaderReading, ReaderWillRead, ReaderRecommend


admin.site.register(Book)
admin.site.register(BookAuthor)
admin.site.register(BookReview)
admin.site.register(ReaderRead)
admin.site.register(ReaderReading)
admin.site.register(ReaderWillRead)
admin.site.register(ReaderRecommend)
