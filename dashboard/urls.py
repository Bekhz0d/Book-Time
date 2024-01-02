from django.urls import path
from dashboard.views import DashboardView, ConfirmDeleteReaderView, DeleteReaderView, \
    EditReaderView, AddReaderView, ReaderMessagesView, PaymentView, ToPayView, EditPayView


app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('reader/<int:reader_id>/delete/confirm/', ConfirmDeleteReaderView.as_view(), 
         name="delete_reader_confirm"),
    path('reader/<int:reader_id>/delete/', DeleteReaderView.as_view(), name="delete_reader"),
    path('reader/<int:reader_id>/edit/', EditReaderView.as_view(), name="edit_reader"),
    path('add/reader/', AddReaderView.as_view(), name="add_reader"),
    path('reader/<int:reader_id>/messages/', ReaderMessagesView.as_view(), name="reader_messages"),
    path('reader/<int:reader_id>/payment/', PaymentView.as_view(), name="payment"),
    path('reader/<int:reader_id>/to_pay/', ToPayView.as_view(), name="to_pay"),
    path('reader/<int:reader_id>/edit_pay/', EditPayView.as_view(), name="edit_pay"),
]
