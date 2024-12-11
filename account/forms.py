from django import forms
from .models import Deposit
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id': 'required'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id': 'required'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id': 'required'}))
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'birthday']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            # Create a Deposit object for the user
            account_no = 11000 + user.id  # Default account number logic
            Deposit.objects.create(user=user, account_no=account_no)

        return user


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['balance']

