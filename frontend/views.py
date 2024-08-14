import requests
import os
from django.template import Template, Context
from django.http import HttpResponse, Http404
from django.conf import settings

def render_template_from_api(request, template_id):
    # Endpoint de la API para obtener la información del template
    api_url = f"http://localhost:8000/api/templates/{template_id}/"
    projects_api_url = "http://localhost:8000/api/projects/"  # Endpoint de la API para obtener los proyectos
    
    # Hacer la solicitud a la API para el template
    response = requests.get(api_url)
    
    if response.status_code == 200:
        template_data = response.json()

        # Hacer la solicitud a la API para los proyectos
        projects_response = requests.get(projects_api_url)
        
        if projects_response.status_code == 200:
            projects_data = projects_response.json()
        else:
            projects_data = []  # Si falla, usar una lista vacía

        # Obtener el path relativo a partir de la URL de archivo
        template_file_url = template_data['html_file']
        template_file_path = os.path.join(settings.MEDIA_ROOT, template_file_url.split(settings.MEDIA_URL)[-1])

        try:
            with open(template_file_path, 'r') as file:
                template_content = file.read()
        except FileNotFoundError:
            raise Http404("Template file not found")
        
        # Crear un objeto Template de Django
        django_template = Template(template_content)
        
        # Renderizar el template con el contexto deseado
        context = {
            'template': template_data,
            'colors': template_data.get('colors', {}),
            'hero_image': template_data.get('hero_image', {}),
            'projects': projects_data,  # Añadir los proyectos al contexto
        }
        rendered_content = django_template.render(Context(context))
        
        # Devolver la respuesta HTTP con el contenido renderizado
        return HttpResponse(rendered_content)
    
    else:
        # Si no se encuentra el template, lanzar un 404
        raise Http404("Template not found")
