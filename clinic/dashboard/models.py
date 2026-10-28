from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='patient_profile',
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    weight = models.FloatField(help_text='kg')
    height = models.FloatField(help_text='cm')
    cf = models.CharField(max_length=16, unique=True, help_text='Codice Fiscale')

    class Meta:
        ordering = ['last_name', 'first_name', 'date_of_birth']
        permissions = (("can_view_patient", "Can view patient"),)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
        
    def get_absolute_url(self):
        return reverse('patient-detail', args=[str(self.id)])

class Doctor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='doctor_profile'
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    id_doctor = models.CharField(max_length=10, unique=True, help_text='ID Doctor')
    date_of_birth = models.DateField()
    
    class Meta:
        ordering = ['specialization', 'last_name', 'first_name', 'id_doctor']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  
    
    def get_absolute_url(self):
        return reverse('doctor-detail', args=[str(self.id)])


class Treatment(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=False,null=False)
    cost = models.DecimalField(max_digits=8, decimal_places=2, help_text='€')
    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"
    
    def get_absolute_url(self):
        return reverse('treatment-detail', args=[str(self.id)])
    
class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    ambulatory = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        ordering = ['patient','date', 'time']
        permissions = (("can_view_visit", "Can view visit"),)

    def __str__(self):
        return f"Visit of {self.patient} with {self.doctor} on {self.date} at {self.time}"
    
    def get_absolute_url(self):
        return reverse('visit-detail', args=[str(self.id)])