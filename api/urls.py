from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ColorsViewSet, TemplateViewSet
from curriculum.views import ProfileViewSet, SkillViewSet, LanguageViewSet, InterestViewSet, EducationViewSet, ExperienceViewSet, ProjectViewSet

router = DefaultRouter()
router.register(r'colors', ColorsViewSet)
router.register(r'templates', TemplateViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'languages', LanguageViewSet)
router.register(r'interests', InterestViewSet)
router.register(r'educations', EducationViewSet)
router.register(r'experiences', ExperienceViewSet)
router.register(r'projects', ProjectViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
