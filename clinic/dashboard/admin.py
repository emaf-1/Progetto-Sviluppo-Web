from django.contrib import admin
from .models import Patient, Doctor, Treatment, Visit

from django.contrib import admin

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'specialization', 'date_of_birth', 'id_doctor')
    fieldsets = (('identifier', {'fields':('id_doctor',)}),('Anagrafica Medico', {'fields': (('first_name', 'last_name'), 'date_of_birth')}),('Specializzazione', {'fields': ('specialization',)}),)

class VisitInline(admin.TabularInline):
    extra = 0
    model = Visit
    fields = ('doctor', 'treatment', 'date', 'time', 'ambulatory')

class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'weight', 'height', 'cf', 'user')
    fieldsets = (('Dati Fiscali', {'fields': ('cf',)}),('Dati Personali', {'fields': (('first_name', 'last_name'),)}),('Parametri Medici e Nascita', {'fields': (('date_of_birth', 'weight', 'height'),),}),)
    inlines = [VisitInline]

class PatientInTreatmentInline(admin.TabularInline):
    extra = 0
    model = Visit
    fields = ('patient', 'date', 'time', 'doctor', 'ambulatory')
    ordering = ('date', 'time')

class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'cost')
    fieldsets = (('Informazioni Trattamento', {'fields': ('name', 'description')}),('Aspetto Economico', {'fields': ('cost',)}),)
    inlines = [PatientInTreatmentInline]

class VisitAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'treatment', 'date', 'time', 'ambulatory')
    fieldsets = (
        ('Attori Coinvolti', {'fields': (('patient', 'doctor', 'treatment'),)}),('Dettagli Appuntamento', {'fields': (('date', 'time', 'ambulatory'),)}),)


admin.site.register(Visit, VisitAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Treatment, TreatmentAdmin)

# Register your models here.

