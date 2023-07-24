from django import forms
from .models import Movie
from django import forms


class RangeInput(forms.NumberInput):
    input_type = 'range'


class SearchFormDB(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('name', 'director', 'genre')

        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Поиск по названию'
            }),
            'director': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Поиск по режиссеру'
            }),
            'genre': forms.SelectMultiple(attrs={
                'class': "form-control ,text-dark",
                'placeholder': 'Поиск по жанру'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

