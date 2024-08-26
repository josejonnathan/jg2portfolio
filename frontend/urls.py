from django.urls import path
from .views import CurriculumDetailView


urlpatterns = [
    path('curriculum/<int:pk>/', CurriculumDetailView.as_view(), name='curriculum_detail'),
    
]
