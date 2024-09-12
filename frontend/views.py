import qrcode
import base64
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from io import BytesIO
from django.views.generic import DetailView
from curriculum.models import Profile
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseForbidden
from api.models import Template
import random


def home_view(request):
    # Obtén todos los templates disponibles
    templates = Template.objects.all()

    if templates.exists():
        # Selecciona un template aleatorio
        selected_template = random.choice(templates)
    else:
        # Usa valores por defecto si no hay templates disponibles
        selected_template = None

    # Prepara el contexto para el template
    context = {
        'selected_template': selected_template,
    }

    # Renderiza la página de inicio usando un template genérico
    return render(request, 'home.html', context)


class CurriculumDetailView(DetailView):
    model = Profile
    context_object_name = 'profile'

    def get_template_names(self):
        # Obtener el template HTML del perfil
        profile = self.get_object()
        if profile.htmltemplate:
            # Devuelve el nombre del archivo HTMLTemplate si está configurado
            return [profile.htmltemplate.html.path]
        else:
            # Devuelve el template por defecto si no se seleccionó HTMLTemplate
            return ['curriculum_detail.html']

    def get(self, request, *args, **kwargs):
        profile = self.get_object()

        # Verificar si el usuario autenticado es el propietario del currículum
        if request.user.is_authenticated and profile.user == request.user:
            # El usuario es el propietario, continuar sin comprobar la contraseña
            return super().get(request, *args, **kwargs)

        # Verificar si el currículum está protegido por contraseña
        if profile.password_protected:
            password = request.GET.get('password')
            
            if not password:
                # Si no se ha proporcionado la contraseña, mostrar un formulario de contraseña
                return render(request, 'password_prompt.html', {'profile': profile})

            if password != profile.password:
                # Si la contraseña es incorrecta, redirigir a la página 'wrong-password' con el pk del perfil
                return redirect('wrong_password', pk=profile.pk)
        
        # Si no hay contraseña o si la contraseña es correcta, continuar mostrando el currículum
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()

        # URL de la página del currículum
        page_url = self.request.build_absolute_uri(self.request.path)

        # Generar el código QR
        qr_code = qrcode.make(page_url)
        qr_code_io = BytesIO()
        qr_code.save(qr_code_io, format='PNG')
        qr_code_io.seek(0)

        # Convertir el código QR a base64
        qr_code_base64 = base64.b64encode(qr_code_io.getvalue()).decode()
        context['qr_code'] = qr_code_base64

        # Generar enlaces para compartir en redes sociales
        context['share_facebook'] = f"https://www.facebook.com/sharer/sharer.php?u={page_url}"
        context['share_twitter'] = f"https://twitter.com/intent/tweet?url={page_url}&text=Check out this CV"
        context['share_linkedin'] = f"https://www.linkedin.com/sharing/share-offsite/?url={page_url}"
        context['share_whatsapp'] = f"https://api.whatsapp.com/send?text=Check out this CV {page_url}"
        context['share_telegram'] = f"https://telegram.me/share/url?url={page_url}&text=Check out this CV"

        # Otras variables de contexto basadas en el template seleccionado
        if profile.template and profile.template.text_light:
            context['text_color'] = 'white'
            context['background_color_primary'] = profile.template.colors.primary
            context['background_color_secondary'] = profile.template.colors.secondary
            context['background_color_tertiary'] = profile.template.colors.tertiary
        else:
            context['text_color'] = 'black'
            context['background_color_primary'] = profile.template.colors.primary if profile.template else "#ffffff"
            context['background_color_secondary'] = profile.template.colors.secondary if profile.template else "#f8f9fa"
            context['background_color_tertiary'] = profile.template.colors.tertiary if profile.template else "#e9ecef"

        context['skills'] = profile.skills.all()
        context['languages'] = profile.languages.all()
        context['interests'] = profile.interests.all()
        context['projects'] = profile.projects.all().order_by('-end_date')
        context['education'] = profile.education.all().order_by('-end_date')
        context['experience'] = profile.experience.all().order_by('-end_date')

        return context


def wrong_password(request, pk):
    return render(request, 'wrong_password.html', {'pk': pk})

def TermsAndConditionsView(request):
    return render(request, 'terms_and_conditions.html')

def TurorialView(request):
    return render(request, 'tutorial.html')

# SEO

def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
        "Allow: /",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def cookies(request):
    cookies = request.COOKIES  # Get all the cookies
    cookie_list = []

    # Example of how you might structure cookie information
    for cookie_name, cookie_value in cookies.items():
        if cookie_name == 'sessionid':
            cookie_list.append({
                'name': 'sessionid',
                'type': 'Strictly necessary',
                'purpose': 'Keeps the user\'s session active',
                'duration': 'Session'
            })
        elif cookie_name == 'csrftoken':
            cookie_list.append({
                'name': 'csrftoken',
                'type': 'Strictly necessary',
                'purpose': 'Protects against CSRF attacks',
                'duration': '1 year'
            })
        # Add more cookies as needed
        else:
            cookie_list.append({
                'name': cookie_name,
                'type': 'Other',
                'purpose': 'Unknown',
                'duration': 'Unknown'
            })

    context = {
        'cookies': cookie_list,
    }

    return render(request, 'cookies.html', context)