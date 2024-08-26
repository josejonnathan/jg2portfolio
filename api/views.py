
from rest_framework import viewsets, permissions
from .models import Template, Colors
from .serializers import TemplateSerializer, ColorsSerializer



class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Permite el acceso a cualquier usuario

class ColorsViewSet(viewsets.ModelViewSet):
    queryset = Colors.objects.all()
    serializer_class = ColorsSerializer
    permission_classes = [permissions.AllowAny]  # Permite la creación de entradas por cualquier usuario

