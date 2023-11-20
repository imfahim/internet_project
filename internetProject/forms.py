from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['first_name', 'last_name','card_number', 'card_expiry_month', 'card_expiry_year', 'card_cvc']

    widgets = {
        'first_name' : forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John'})),
        'last_name' : forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe'})),
        'card_number' : forms.CharField(label='Card Number', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 5678 9012 3456'})),
        'card_expiry_month' : forms.CharField(label='Expiration Month', widget=forms.Select(attrs={'class': 'form-control'}, choices=[(str(i).zfill(2), str(i).zfill(2)) for i in range(1, 13)])),
        'card_expiry_year' : forms.CharField(label='Expiration Year', widget=forms.Select(attrs={'class': 'form-control'}, choices=[(str(i), str(i)) for i in range(2023, 2033)])),
        'card_cvc' : forms.CharField(label='CVC', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123'})),

    }
