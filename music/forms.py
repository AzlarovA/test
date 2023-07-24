from django import forms
from .models import Music
from django import forms


class RangeInput(forms.NumberInput):
    input_type = 'range'


class SearchFormDB(forms.ModelForm):
    created_at_from = forms.IntegerField(widget=RangeInput(attrs={
        'class': "form-control",
        'min': 1900,
        'max': 2023,
    }), required=False)
    created_at_to = forms.IntegerField(widget=RangeInput(attrs={
        'class': "form-control",
        'min': 1900,
        'max': 2023,
    }), required=False)

    class Meta:
        model = Music
        fields = ('title', 'author', 'genre')

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
                'class': "form-control",
                'placeholder': 'Поиск по жанру'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

