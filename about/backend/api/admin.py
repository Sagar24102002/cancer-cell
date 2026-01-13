from django.contrib import admin
from .models import Patient, Sample, GeneExpression, Treatment

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth')

@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = ('patient', 'sample_type', 'collected_date')

@admin.register(GeneExpression)
class GeneExpressionAdmin(admin.ModelAdmin):
    list_display = ('gene_name', 'expression_value', 'sample')

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'treatment_name', 'start_date')
