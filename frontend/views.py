from django.shortcuts import render
from api.models import Project, Template
import random

def home_view(request):
    projects = Project.objects.all()  # Obtén todos los proyectos de la base de datos
    templates = Template.objects.all()  # Obtén todos los templates de la base de datos

    if templates.exists():  # Verifica si hay templates disponibles
        selected_template = random.choice(templates)  # Selecciona un template aleatorio
    else:
        selected_template = None  # Maneja el caso en el que no haya templates

    context = {
        'projects': projects,
        'selected_template': selected_template,
    }

    return render(request, 'home.html', context)  # Renderiza un template por defecto si no hay templates
