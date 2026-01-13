from rest_framework import viewsets
from .models import Patient, Sample, GeneExpression, Treatment
from .serializers import PatientSerializer, SampleSerializer, GeneExpressionSerializer, TreatmentSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class SampleViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer

class GeneExpressionViewSet(viewsets.ModelViewSet):
    queryset = GeneExpression.objects.all()
    serializer_class = GeneExpressionSerializer

class TreatmentViewSet(viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
