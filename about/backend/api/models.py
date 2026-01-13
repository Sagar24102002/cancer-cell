from django.db import models

class Patient(models.Model):
    SEX_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='O')
    diagnosis_date = models.DateField(null=True, blank=True)
    diagnosis = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Sample(models.Model):
    SAMPLE_TYPES = [('TUMOR', 'Tumor'), ('NORMAL', 'Normal'), ('BLOOD', 'Blood')]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='samples')
    sample_type = models.CharField(max_length=10, choices=SAMPLE_TYPES)
    collected_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.patient} - {self.sample_type} ({self.id})"

class GeneExpression(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='expressions')
    gene_name = models.CharField(max_length=200)
    expression_value = models.FloatField()

    def __str__(self):
        return f"{self.gene_name}: {self.expression_value}"

class Treatment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='treatments')
    treatment_name = models.CharField(max_length=200)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    outcome = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient} - {self.treatment_name}"
