from rest_framework import viewsets
from .models import HeroImage, Colors, Template, Project
from .serializers import HeroImageSerializer, ColorsSerializer, TemplateSerializer, ProjectSerializer

class HeroImageViewSet(viewsets.ModelViewSet):
    queryset = HeroImage.objects.all()
    serializer_class = HeroImageSerializer

class ColorsViewSet(viewsets.ModelViewSet):
    queryset = Colors.objects.all()
    serializer_class = ColorsSerializer

class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
