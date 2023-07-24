from django import forms
from .models import Users
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


class LoginForm(forms.ModelForm):
    username = forms.CharField(label='Юзернейм', max_length=100)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ['username','password1']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': "form-control",
            }),
            'password1': forms.PasswordInput(attrs={
                'class': "form-control",
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('Неверный юзернейм или пароль')
        return cleaned_data


class UsersForm(forms.ModelForm):
    username = forms.CharField(label='Юзернейм', max_length=100)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ['nickname', 'email']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': '@Nagibator'
            }),
            'nickname': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Nagiyeb'
            }),
            'email': forms.EmailInput(attrs={
                'class': "form-control",
                'placeholder': 'nagiyeb@gmail.com'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': "form-control",
            }),
            'password2': forms.PasswordInput(attrs={
                'class': "form-control",
            })
        }

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )
        user.save()
        user_profile = super().save(commit=False)
        user_profile.user = user
        if commit:
            user_profile.save()
        return user_profile

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким имейлом уже существует')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким юзернейм уже существует')
        return username


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(label='Юзернейм', max_length=100)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput, required=False)
    image = forms.ImageField(label='Изображение', required=False)

    class Meta:
        model = Users
        fields = ['nickname', 'email']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': '@Nagibator'
            }),
            'nickname': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Nagiyeb'
            }),
            'email': forms.EmailInput(attrs={
                'class': "form-control",
                'placeholder': 'nagiyeb@gmail.com'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': "form-control",
            }),
            'password2': forms.PasswordInput(attrs={
                'class': "form-control",
            })
        }

    def save(self, commit=True):
        user = self.instance.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        if password:
            user.set_password(password)
        user.save()
        user_profile = super().save(commit=False)
        user_profile.user = user
        image = self.cleaned_data.get('image')
        if image:
            user_profile.image = image
        if commit:
            user_profile.save()
        return user_profile

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance and self.instance.email == email:
            return email
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким имейлом уже существует')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance and self.instance.user.username == username:
            return username
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким юзернейм уже существует')
        return username


class EmailConfirmationForm(forms.Form):
    code = forms.CharField(label='Код подтверждения', max_length=6)