import qrcode
import base64
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from io import BytesIO
from django.views.generic import DetailView
from curriculum.models import Profile
from django.shortcuts import render


def home_view(request):
    return render(request, 'home.html')


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
        context['projects'] = profile.projects.all()
        context['education'] = profile.education.all()
        context['experience'] = profile.experience.all()

        return context
