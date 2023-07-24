from django import forms
from .models import ContactPageForm


class ContactFormDB(forms.ModelForm):
    class Meta:
        model = ContactPageForm
        fields = ('first_name', 'last_name', 'email','subject', 'message')

        widgets = {
            'subject': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Your subject of this message'
            }),
            'first_name': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Your firstname'
            }),
            'last_name': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Your lastname'
            }),
            'email': forms.EmailInput(attrs={
                'class': "form-control",
                'placeholder': 'Your email address'
            }),
            'message': forms.Textarea(attrs={
                'class': "form-control",
                'placeholder': 'Say something about us'
            }),
        }
