from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HeroImageViewSet, ColorsViewSet, TemplateViewSet, ProjectViewSet

router = DefaultRouter()
router.register(r'hero-images', HeroImageViewSet)
router.register(r'colors', ColorsViewSet)
router.register(r'templates', TemplateViewSet)
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
