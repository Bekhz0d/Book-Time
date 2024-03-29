from django import forms
from readers.models import Readers


class ReaderCreateForm(forms.ModelForm):
    class Meta:
        model = Readers
        fields = ("username", "first_name", "last_name", "email", "password")

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data["password"])
        user.save()

        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Readers
        fields = ['username', 'first_name', 'last_name', 'email', 'picture']
