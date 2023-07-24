from django import forms
from .models import Question, Answer
from django.core.validators import MaxLengthValidator, MaxValueValidator


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'genre', 'image', 'files', 'content')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': "form-control",
            }),
            'content': forms.Textarea(attrs={
                'class': "form-control",
            }),
            'genre': forms.SelectMultiple(attrs={
                'class': "form-control",
            }),
            'image': forms.FileInput(attrs={
                'class': "form-control",
                'placeholder': 'Выберите изображение если надо'
            }),
            'files': forms.FileInput(attrs={
                'class': "form-control",
                'placeholder': 'Выберите файл если надо'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].validators.append(MaxLengthValidator(100))

    def clean_genre(self):
        data = self.cleaned_data['genre']
        if len(data) > 5:
            raise forms.ValidationError("Вы можете выбрать не более 5 тегов.")
        return data


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('content', 'image', 'files',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': "form-control",
            }),
            'image': forms.FileInput(attrs={
                'class': "form-control",
                'placeholder': 'Выберите изображение если надо'
            }),
            'files': forms.FileInput(attrs={
                'class': "form-control",
                'placeholder': 'Выберите файл если надо'
            }),
        }
