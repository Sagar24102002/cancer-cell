from rest_framework import serializers
from .models import Patient, Sample, GeneExpression, Treatment

class GeneExpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneExpression
        fields = '__all__'

class SampleSerializer(serializers.ModelSerializer):
    expressions = GeneExpressionSerializer(many=True, read_only=True)

    class Meta:
        model = Sample
        fields = '__all__'

class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    samples = SampleSerializer(many=True, read_only=True)
    treatments = TreatmentSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'
