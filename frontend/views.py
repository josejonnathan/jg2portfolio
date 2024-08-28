import qrcode
import base64
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from io import BytesIO
from django.views.generic import DetailView
from curriculum.models import Profile

class CurriculumDetailView(DetailView):
    model = Profile
    template_name = 'curriculum_detail2.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()

        # URL de la página del currículum
        page_url = self.request.build_absolute_uri(self.request.path)

        # Generar el código QR
        qr_url = self.request.build_absolute_uri(self.request.path)  # URL completa a la vista detallada
        qr_code = qrcode.make(qr_url)
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

        # Otras variables de contexto
        if profile.template.text_light:
            context['text_color'] = 'white'
            context['background_color_primary'] = profile.template.colors.primary
            context['background_color_secondary'] = profile.template.colors.secondary
            context['background_color_tertiary'] = profile.template.colors.tertiary
        else:
            context['text_color'] = 'black'
            context['background_color_primary'] = profile.template.colors.primary
            context['background_color_secondary'] = profile.template.colors.secondary
            context['background_color_tertiary'] = profile.template.colors.tertiary

        context['skills'] = profile.skills.all()
        context['languages'] = profile.languages.all()
        context['interests'] = profile.interests.all()
        context['projects'] = profile.projects.all()
        context['education'] = profile.education.all()
        context['experience'] = profile.experience.all()

        return context
