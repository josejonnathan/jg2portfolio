from django.urls import path
from .views import  CurriculumDetailView, home_view, TermsAndConditionsView, robots_txt, wrong_password, TurorialView


urlpatterns = [
    path('', home_view, name='home'),
    path('curriculum/<int:pk>/', CurriculumDetailView.as_view(), name='curriculum_detail'),
    path('wrong_password/<int:pk>/', wrong_password, name='wrong_password'),
    path('terms/', TermsAndConditionsView, name='terms'),
    path('tutorial/', TurorialView, name='tutorial'),
    path('robots.txt', robots_txt, name='robots_txt'),

    
]
