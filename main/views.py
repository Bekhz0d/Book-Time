from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
# from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from main.forms import BookReviewForm
from main.models import Book, BookReview
from django.core.paginator import Paginator
from django.contrib import messages


class BooksView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')

        search_query = request.GET.get('q', '')
        if search_query:
            books = books.filter(title__icontains=search_query)

        page_size = request.GET.get('page_size', 5)
        paginator = Paginator(books, page_size)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        return render(request, "books/list.html", {"page_obj": page_obj, "search_query": search_query})


class BookDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm()

        return render(request, "books/detail.html", {"book": book, "review_form": review_form})    
        

class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm(data=request.POST)

        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                reader=request.user,
                stars_given=review_form.cleaned_data['stars_given'],
                comment=review_form.cleaned_data['comment']
            )

            return redirect(reverse('main:detail_page', kwargs={'id': book.id}))
        return render(request, 'books/detail.html', {'book': book, 'review_form': review_form})


class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review)

        return render(request, 'books/edit_review.html', {'book': book,
                                                        'review': review, 
                                                        'review_form': review_form})
    
    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review, data=request.POST)

        if review_form.is_valid():
            review_form.save()
            return redirect(reverse('main:detail_page', kwargs={'id': book.id}))
        
        return render(request, 'books/edit-review.html', {"book": book,
                                                          "review": review, 
                                                          "review_form": review_form})


class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        return render(request, 'books/confirm_delete_review.html', {"book": book, 'review': review})
    

class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)

        review.delete()
        messages.success(request, 'You have successfully deleted the review')

        return redirect(reverse('main:detail_page', kwargs={'id': book.id}))
     