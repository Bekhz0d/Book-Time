from django.db import models
from readers.models import Readers

class ReaderMessages(models.Model):
    reader = models.ForeignKey(Readers, related_name='reader_messages', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(Readers, related_name='admin_messsages', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.admin.username} sent message to {self.reader.username}"
    