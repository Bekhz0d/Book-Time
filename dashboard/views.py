from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import UserPassesTestMixin
from readers.models import Readers, Payment
from django.contrib import messages
from django.urls import reverse
from dashboard.forms import ReaderUpdateForm, ReaderCreateForm, MessageForm, PaymentForm
from django.db.models import Q
from dashboard.models import ReaderMessages
from django.utils import timezone



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
    

# class StatusNewView(View):
#     def get(self, request):
#         readers = Readers.objects.filter(status="New")

#         search_query = request.GET.get('q', '')
#         if search_query:
#             readers = readers.filter(
#                 Q(username__icontains=search_query) | 
#                 Q(first_name__icontains=search_query) |
#                 Q(last_name__icontains=search_query) |
#                 Q(phone__icontains=search_query) |
#                 Q(address__icontains=search_query) |
#                 Q(email__icontains=search_query)
#                 )
#         context = {"readers": readers, "search_query": search_query}

#         return render(request, 'dashboard/dashboard.html', context)


# class StatusActiveView(View):
#     def get(self, request):
#         readers = Readers.objects.filter(status="Active")

#         search_query = request.GET.get('q', '')
#         if search_query:
#             readers = readers.filter(
#                 Q(username__icontains=search_query) | 
#                 Q(first_name__icontains=search_query) |
#                 Q(last_name__icontains=search_query) |
#                 Q(phone__icontains=search_query) |
#                 Q(address__icontains=search_query) |
#                 Q(email__icontains=search_query)
#                 )
#         context = {"readers": readers, "search_query": search_query}

#         return render(request, 'dashboard/dashboard.html', context)


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



class AddReaderView(SuperuserRequiredMixin, View):
    def get(self, request):
        add_reader_form = ReaderCreateForm()
        
        return render(request, 'dashboard/add_reader.html', {'add_reader_form': add_reader_form})

    def post(self, request):
        add_reader_form = ReaderCreateForm(data=request.POST)

        if add_reader_form.is_valid():
            add_reader_form.save()
            return redirect(reverse('dashboard:dashboard'))
        
        return render(request, 'dashboard/add_reader.html', {'add_reader_form': add_reader_form})


class ReaderMessagesView(SuperuserRequiredMixin, View):
    def get(self, request, reader_id):
        reader = Readers.objects.get(id=reader_id)
        reader_messages = reader.reader_messages.all()
        message_form = MessageForm()
        context = {'reader': reader, 'message_form': message_form, 'reader_messages': reader_messages}

        return render(request, 'dashboard/messages.html', context)

    def post(self, request, reader_id):
        reader = Readers.objects.get(id=reader_id)
        message_form = MessageForm(data=request.POST)
        reader_messages = ReaderMessages.objects.filter(reader=reader)
        context = {'reader': reader, 'message_form': message_form, 'reader_messages': reader_messages}

        if message_form.is_valid():
            reader_messages_create = ReaderMessages.objects.create(admin=request.user,
                                                                   reader=reader,
                                                                   text=message_form.cleaned_data['text'])
            reader_messages_create.save()

            return redirect(reverse('dashboard:reader_messages', kwargs={'reader_id': reader_id}))
        return render(request, 'dashboard/messages.html', context)


class PaymentView(SuperuserRequiredMixin, View):
    def get(self, request, reader_id):
        reader = Readers.objects.get(id=reader_id)
        last_payments = reader.payment_reader.all().order_by('-payment_date')

        context = {'reader': reader, 'last_payments': last_payments}

        return render(request, 'dashboard/payments.html', context)
    

class ToPayView(SuperuserRequiredMixin, View):
    def get(self, request, reader_id):
        pay_form = PaymentForm()
        context = {'pay_form': pay_form}

        return render(request, 'dashboard/to_pay.html', context)
    
    def post(self, request, reader_id):
        reader = Readers.objects.get(id=reader_id)
        pay_form = PaymentForm(data=request.POST)
        context = {'reader': reader, 'pay_form': pay_form}

        if pay_form.is_valid():
            Payment.objects.create(reader=reader,
                                             payment_amount=pay_form.cleaned_data['payment_amount'],
                                             payee=request.user)
            reader.balance += pay_form.cleaned_data['payment_amount']
            reader.status = "Active"
            reader.save()
            return redirect(reverse('dashboard:payment', kwargs={'reader_id': reader_id}))
        return render(request, 'dashboard/payments.html', context)
    


class EditPayView(SuperuserRequiredMixin, View):
    def get(self, request, reader_id):
        reader = Readers.objects.get(id=reader_id)
        last_payment = reader.payment_reader.last()
        edit_form = PaymentForm(instance=last_payment)
        context = {'edit_form': edit_form}
        return render(request, 'dashboard/edit_pay.html', context)
    
    def post(self, request, reader_id):
        reader = Readers.objects.get(id=reader_id)
        edit_form = PaymentForm(data=request.POST)
        last_payment = reader.payment_reader.last()
        context = {'edit_form': edit_form}

        if edit_form.is_valid():
            Payment.objects.filter(payment_amount=last_payment.payment_amount).update(
                payment_amount=edit_form.cleaned_data['payment_amount'],
                payment_edited = True,
                payment_update_date=timezone.now())
            reader.balance = reader.balance - last_payment.payment_amount + edit_form.cleaned_data['payment_amount']
            reader.save() 
            return redirect(reverse('dashboard:payment', kwargs={'reader_id': reader_id}))
        return render(request, 'dashboard/payments.html', context)
    