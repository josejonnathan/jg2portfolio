from django.urls import path
from .views import  CurriculumDetailView, home_view, TermsAndConditionsView


urlpatterns = [
    path('', home_view, name='home'),
    path('curriculum/<int:pk>/', CurriculumDetailView.as_view(), name='curriculum_detail'),
    path('terms/', TermsAndConditionsView, name='terms'),
    
]
