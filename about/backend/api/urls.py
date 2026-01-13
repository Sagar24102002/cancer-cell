from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, SampleViewSet, GeneExpressionViewSet, TreatmentViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'samples', SampleViewSet)
router.register(r'expressions', GeneExpressionViewSet)
router.register(r'treatments', TreatmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
