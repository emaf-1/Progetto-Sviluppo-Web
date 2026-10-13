from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Visit

class SignUpForm(UserCreationForm):
    date_of_birth = forms.DateField(required=True, label="data di nascita", help_text="formato data YYYY-MM-DD")
    weight = forms.CharField(max_length=4, label='kg')
    height = forms.CharField(max_length=3, label='cm')
    cf = forms.CharField(max_length=16, label='Codice Fiscale')
    class Meta:
        model = User
        fields = ['cf', 'username', 'first_name', 'last_name', 'email',  'date_of_birth', 'weight', 'height','password1', 'password2',]


class ReservationForm(forms.ModelForm):

    class Meta:
        model= Visit
        fields = ['patient','doctor', 'treatment', 'date', 'time', 'ambulatory']
