from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import UserPassesTestMixin
from readers.models import Readers
from django.contrib import messages
from django.urls import reverse
from dashboard.forms import ReaderUpdateForm
from django.db.models import Q


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
    

class DashboardView(SuperuserRequiredMixin, View):
    def get(self, request):
        readers = Readers.objects.all()

        search_query = request.GET.get('q', '')
        if search_query:
            readers = readers.filter(
                Q(username__icontains=search_query) | 
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(phone__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(email__icontains=search_query)
                )
        context = {"readers": readers, "search_query": search_query}

        return render(request, 'dashboard/dashboard.html', context)


class ConfirmDeleteReaderView(SuperuserRequiredMixin, View):
    def get(self, request, reader_id):
        reader = Readers.objects.get(id=reader_id)
        return render(request, 'dashboard/confirm_delete_reader.html', {"reader": reader})
    

class DeleteReaderView(SuperuserRequiredMixin, View):
    def get(self, request, reader_id):
        reader = Readers.objects.get(id=reader_id)

        reader.delete()
        messages.success(request, 'You have successfully deleted reader')

        return redirect(reverse('dashboard:dashboard'))
    

class EditReaderView(SuperuserRequiredMixin, View):
    def get(self, request, reader_id):
        reader = Readers.objects.get(id=reader_id)
        reader_form = ReaderUpdateForm(instance=reader)

        return render(request, 'dashboard/edit_reader.html', {'reader_form': reader_form})
    
    def post(self, request, reader_id):
        reader = Readers.objects.get(id=reader_id)
        reader_form = ReaderUpdateForm(instance=reader, data=request.POST)

        if reader_form.is_valid():
            reader_form.save()
            return redirect(reverse('dashboard:dashboard'))

        return render(request, 'dashboard/edit_reader.html', {'reader_form': reader_form})
