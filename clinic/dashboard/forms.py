from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Patient, Visit
import datetime


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
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # se lo user ha un profilo paziente, il paziente è fisso
        if user is not None and hasattr(user, 'patient_profile'):
            self.instance.patient = user.patient_profile
            del self.fields['patient']
       
    def clean_date(self):
            date = self.cleaned_data.get('date')
            if date and date <= datetime.date.today():
                raise forms.ValidationError("Sorry, you can't reserve a visit in the past")
            return date

    def clean(self):
            cleaned_data = super().clean()
            doctor = cleaned_data.get('doctor')
            date = cleaned_data.get('date')
            time = cleaned_data.get('time')
            if doctor and date and time:
                qs = Visit.objects.filter(doctor=doctor, date=date, time=time)
                if self.instance.pk:
                    qs = qs.exclude(pk=self.instance.pk)
                if qs.exists():
                    raise forms.ValidationError("Doctor is already busy in this time")
            return cleaned_data
    def save(self, commit=True):
        visit = super().save(commit=False)
        if self.patient_obj:
            visit.patient = self.patient_obj
        if commit:
            visit.save()
        return visit
