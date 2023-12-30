from django.contrib import admin
from main.models import Book, Author, BookAuthor, BookReview, ReaderRead, \
    ReaderReading, ReaderWillRead, ReaderRecommend


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'price')
    search_fields = ('title', 'isbn', 'price')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',)
    search_fields = ('first_name', 'last_name', 'email',)


class BookAuthorAdmin(admin.ModelAdmin):
    pass


class BookReviewAdmin(admin.ModelAdmin):
    pass


class ReaderReadAdmin(admin.ModelAdmin):
    pass


class ReaderReadingAdmin(admin.ModelAdmin):
    pass


class ReaderWillReadAdmin(admin.ModelAdmin):
    pass


class ReaderRecommendAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(ReaderRead, ReaderReadAdmin)
admin.site.register(ReaderReading, ReaderReadingAdmin)
admin.site.register(ReaderWillRead, ReaderWillReadAdmin)
admin.site.register(ReaderRecommend, ReaderRecommendAdmin)
