# user/views.py

import qrcode
import base64
from io import BytesIO
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from user.forms import CustomUserCreationForm, ProfileForm, ProfileTemplateForm, SkillForm, LanguageForm, InterestForm, EducationForm, ExperienceForm, ProjectForm
from django.conf import settings
from curriculum.models import Profile 
from curriculum.models import Skill, Language, Interest, Education, Experience, Project
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from api.models import Template
from weasyprint import HTML
from django.templatetags.static import static
from django.utils.translation import activate
from django.utils import translation







def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Desactivar la cuenta hasta que se verifique el correo
            user.save()

            # Crear el perfil relacionado con el usuario
            Profile.objects.create(
                user=user,
                name=user.username,  # Inicializa el nombre con el nombre de usuario
                email=user.email,    # Inicializa el email con el email del usuario
            )

            # Enviar correo de verificación
            mail_subject = 'Activate your account.'
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            message = render_to_string('email_verification.html', {
                'user': user,
                'domain': request.get_host(),
                'uid': uid,
                'token': token,
            })
            
            email = EmailMessage(
                mail_subject,
                message,
                to=[form.cleaned_data.get('email')]
            )
            
            email.content_subtype = "html"  # Cambia a contenido HTML
            email.send()

            messages.success(request, 'Please confirm your email address to complete the registration.')
            return redirect('registration_complete')  # Redirigir a la nueva página de confirmación
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


User = get_user_model()



def registration_complete_view(request):
    """Vista para mostrar la página de confirmación de registro."""
    return render(request, 'registration_complete.html')

def activate_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  
        user.save()  
        messages.success(request, 'Your account has been activated successfully!')
        return redirect('activation_complete') 
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('home')


def activation_complete_view(request):
    """Vista para mostrar la página de confirmación de activación."""
    return render(request, 'activation_complete.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('user_detail')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    template_name = 'registration/password_reset_form.html'
    html_email_template_name = 'registration/password_reset_email.html'  # Define la plantilla HTML
    
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        """
        Envía un correo electrónico con alternativas de texto plano y HTML.
        """
        # Renderiza el asunto y el cuerpo del mensaje
        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())  # Elimina los saltos de línea del asunto

        # Renderiza el mensaje en HTML y en texto plano
        html_message = render_to_string(html_email_template_name or email_template_name, context)
        plain_message = strip_tags(html_message)  # Extrae el contenido de texto plano
        
        # Configura el correo con ambas versiones
        email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
        email.attach_alternative(html_message, "text/html")  # Adjunta la versión HTML
        email.send()


#------------------------------------------------------------------------------------------------------------------------#

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user'
    

    def get_object(self):
        # Obtiene el usuario actual autenticado
        return self.request.user

    def get_context_data(self, **kwargs):
        # Obtiene el contexto existente de la vista detallada del usuario
        context = super().get_context_data(**kwargs)
        # Obtiene el perfil del usuario autenticado
        profile = Profile.objects.get(user=self.request.user)

        # Añade el perfil y otros detalles relacionados al contexto
        context['profile'] = profile
        context['skills'] = profile.skills.all()
        context['languages'] = profile.languages.all()
        context['interests'] = profile.interests.all()
        context['projects'] = profile.projects.all().order_by('-end_date')
        context['education'] = profile.education.all().order_by('-end_date')
        context['experience'] = profile.experience.all().order_by('-end_date')

        return context
    

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm  # Usar el formulario personalizado
    template_name = 'profile_update.html'

    def get_object(self):
        # Obtener el perfil del usuario autenticado
        return get_object_or_404(Profile, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir al currículum relacionado con el perfil actualizado
        return reverse('user_detail')
    

class ProfileTemplateUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileTemplateForm
    template_name = 'profile_template_update.html'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Your profile template has been updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir al currículum relacionado con el perfil actualizado
        return reverse('curriculum_detail', kwargs={'pk': self.object.pk})
    

# Skills

# Vista de creación para Skills
class SkillCreateView(LoginRequiredMixin, CreateView):
    model = Skill
    form_class = SkillForm
    template_name = 'skill_form.html'

    def form_valid(self, form):
        # Asociar la nueva habilidad con el perfil del usuario actual
        form.instance.profile = get_object_or_404(Profile, user=self.request.user)
        messages.success(self.request, 'Skill created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir al currículum detallado del perfil actual
        return reverse_lazy('user_detail')

# Vista de actualización para Skills
class SkillUpdateView(LoginRequiredMixin, UpdateView):
    model = Skill
    form_class = SkillForm
    template_name = 'skill_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Skill updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir al currículum detallado del perfil actual
        return reverse_lazy('user_detail')

# Vista de eliminación para Skills
class SkillDeleteView(LoginRequiredMixin, DeleteView):
    model = Skill
    template_name = 'skill_confirm_delete.html'

    def get_success_url(self):
        # Redirigir al currículum detallado del perfil actual
        return reverse_lazy('user_detail')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Skill deleted successfully!')
        return super().delete(request, *args, **kwargs)
    


class LanguageCreateView(LoginRequiredMixin, CreateView):
    model = Language
    form_class = LanguageForm
    template_name = 'language_form.html'

    def form_valid(self, form):
        # Asociar el nuevo idioma con el perfil del usuario actual
        form.instance.profile = get_object_or_404(Profile, user=self.request.user)
        messages.success(self.request, 'Language created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir al currículum detallado del perfil actual
        return reverse_lazy('user_detail')


class LanguageUpdateView(LoginRequiredMixin, UpdateView):
    model = Language
    form_class = LanguageForm
    template_name = 'language_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Language updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir al currículum detallado del perfil actual
        return reverse_lazy('user_detail')
    

class LanguageDeleteView(LoginRequiredMixin, DeleteView):
    model = Language
    template_name = 'language_confirm_delete.html'

    def get_success_url(self):
        # Redirigir al currículum detallado del perfil actual
        return reverse_lazy('user_detail')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Language deleted successfully!')
        return super().delete(request, *args, **kwargs)
    

    
class InterestCreateView(LoginRequiredMixin, CreateView):
    model = Interest
    form_class = InterestForm
    template_name = 'interest_form.html'

    def form_valid(self, form):
        # Asociar el nuevo interés con el perfil del usuario actual
        form.instance.profile = get_object_or_404(Profile, user=self.request.user)
        messages.success(self.request, 'Interest created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir al currículum detallado del perfil actual
        return reverse_lazy('user_detail')
    

class InterestUpdateView(LoginRequiredMixin, UpdateView):
    model = Interest
    form_class = InterestForm
    template_name = 'interest_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Interest updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir al currículum detallado del perfil actual
        return reverse_lazy('user_detail')
    

class InterestDeleteView(LoginRequiredMixin, DeleteView):
    model = Interest
    template_name = 'interest_confirm_delete.html'

    def get_success_url(self):
        # Redirigir al currículum detallado del perfil actual
        return reverse_lazy('user_detail')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Interest deleted successfully!')
        return super().delete(request, *args, **kwargs)


class EducationCreateView(LoginRequiredMixin, CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'education_form.html'

    def form_valid(self, form):
        # Asociar la nueva educación con el perfil del usuario actual
        form.instance.profile = get_object_or_404(Profile, user=self.request.user)
        messages.success(self.request, 'Education created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir al currículum detallado del perfil actual
        return reverse_lazy('user_detail')
    

class EducationUpdateView(LoginRequiredMixin, UpdateView):
    model = Education
    form_class = EducationForm
    template_name = 'education_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Education updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir al currículum detallado del perfil actual
        return reverse_lazy('user_detail')
    

class EducationDeleteView(LoginRequiredMixin, DeleteView):
    model = Education
    template_name = 'education_confirm_delete.html'

    def get_success_url(self):
        # Redirigir al currículum detallado del perfil actual
        return reverse_lazy('user_detail')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Education deleted successfully!')
        return super().delete(request, *args, **kwargs)
    



# Vista de creación para Experience
class ExperienceCreateView(LoginRequiredMixin, CreateView):
    model = Experience
    form_class = ExperienceForm
    template_name = 'experience_form.html'

    def form_valid(self, form):
        # Asociar la nueva experiencia con el perfil del usuario actual
        form.instance.profile = get_object_or_404(Profile, user=self.request.user)
        messages.success(self.request, 'Experience created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir a los detalles del usuario actual
        return reverse_lazy('user_detail')

# Vista de actualización para Experience
class ExperienceUpdateView(LoginRequiredMixin, UpdateView):
    model = Experience
    form_class = ExperienceForm
    template_name = 'experience_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Experience updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir a los detalles del usuario actual
        return reverse_lazy('user_detail')

# Vista de eliminación para Experience
class ExperienceDeleteView(LoginRequiredMixin, DeleteView):
    model = Experience
    template_name = 'experience_confirm_delete.html'

    def get_success_url(self):
        # Redirigir a los detalles del usuario actual
        return reverse_lazy('user_detail')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Experience deleted successfully!')
        return super().delete(request, *args, **kwargs)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_form.html'

    def form_valid(self, form):
        # Asociar el nuevo proyecto con el perfil del usuario actual
        form.instance.profile = get_object_or_404(Profile, user=self.request.user)
        messages.success(self.request, 'Project created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir a los detalles del usuario actual
        return reverse_lazy('user_detail')
    

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Project updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir a los detalles del usuario actual
        return reverse_lazy('user_detail')
    


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'project_confirm_delete.html'

    def get_success_url(self):
        # Redirigir a los detalles del usuario actual
        return reverse_lazy('user_detail')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Project deleted successfully!')
        return super().delete(request, *args, **kwargs)
    

class TemplateSelectionView(TemplateView):
    template_name = 'template_selection.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['templates'] = Template.objects.all()  
        return context
    

def select_template(request, template_id):
    # Obtener el template seleccionado por el usuario
    template = get_object_or_404(Template, id=template_id)
    
    # Obtener el perfil del usuario autenticado
    profile = get_object_or_404(Profile, user=request.user)
    
    # Asignar el template seleccionado al perfil del usuario y guardar
    profile.template = template
    profile.save()
    
    # Mensaje de éxito para la selección del template
    messages.success(request, 'Template selected successfully!')
    
    # Redirigir al 'curriculum_detail' usando el pk del perfil
    return redirect(reverse('curriculum_detail', kwargs={'pk': profile.pk}))


# PDF
def download_pdf(request, pk):
    # Obtener el perfil del currículum a partir del ID (pk)
    profile = get_object_or_404(Profile, pk=pk)
    
    # Recopilar los mismos datos de contexto que en `CurriculumDetailView`
    skills = profile.skills.all()
    languages = profile.languages.all()
    interests = profile.interests.all()
    projects = profile.projects.all()
    education = profile.education.all()
    experience = profile.experience.all()

    # Generar el código QR en base64
    page_url = request.build_absolute_uri()  # URL actual de la página
    qr_code_img = qrcode.make(page_url)
    qr_code_io = BytesIO()
    qr_code_img.save(qr_code_io, format='PNG')
    qr_code_base64 = base64.b64encode(qr_code_io.getvalue()).decode()

    # Generar URLs absolutas para las imágenes estáticas
    profile_picture_url = request.build_absolute_uri(profile.picture.url) if profile.picture else None
    static_images = {
        'web': request.build_absolute_uri(static('images/website.png')),
        'instagram': request.build_absolute_uri(static('images/instagram.png')),
        'facebook': request.build_absolute_uri(static('images/facebook.png')),
        'linkedin': request.build_absolute_uri(static('images/linkedin.png')),
        'git': request.build_absolute_uri(static('images/git.png')),
        'twitter': request.build_absolute_uri(static('images/x.png')),
    }

    # Renderizar la plantilla 'curriculum_detail_pdf.html'
    html_string = render_to_string('curriculum_detail_pdf.html', {
        'profile': profile,
        'profile_picture_url': profile_picture_url,
        'static_images': static_images,
        'qr_code': qr_code_base64,  # Pasar el código QR en base64
        'skills': skills,
        'languages': languages,
        'interests': interests,
        'projects': projects,
        'education': education,
        'experience': experience,
    })

    # Convertir el HTML a PDF usando WeasyPrint
    pdf_file = HTML(string=html_string).write_pdf()

    # Devolver el PDF como respuesta
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cv_usuario.pdf"'
    return response