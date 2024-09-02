# user/views.py

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from user.forms import CustomUserCreationForm, ProfileForm, ProfileTemplateForm, SkillForm
from django.conf import settings
from curriculum.models import Profile 
from curriculum.models import Skill, Language, Interest, Education, Experience, Project
from django.views.generic import ListView, CreateView, UpdateView, DeleteView



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
            email = EmailMessage(mail_subject, message, to=[form.cleaned_data.get('email')])
            email.send()

            messages.success(request, 'Please confirm your email address to complete the registration.')
            return redirect('registration_complete')  # Redirigir a la nueva página de confirmación
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

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
        return redirect('activation_complete')  # Redirigir a la nueva página de confirmación de activación
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
        context['projects'] = profile.projects.all()
        context['education'] = profile.education.all()
        context['experience'] = profile.experience.all()

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
        return reverse('curriculum_detail', kwargs={'pk': self.object.pk})
    

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
        return reverse_lazy('curriculum_detail', kwargs={'pk': self.object.profile.pk})

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
        return reverse_lazy('curriculum_detail', kwargs={'pk': self.object.profile.pk})

# Vista de eliminación para Skills
class SkillDeleteView(LoginRequiredMixin, DeleteView):
    model = Skill
    template_name = 'skill_confirm_delete.html'

    def get_success_url(self):
        # Redirigir al currículum detallado del perfil actual
        return reverse_lazy('curriculum_detail', kwargs={'pk': self.object.profile.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Skill deleted successfully!')
        return super().delete(request, *args, **kwargs)
    


# Vista de lista para Languages
class LanguageListView(LoginRequiredMixin, ListView):
    model = Language
    template_name = 'language_list.html'

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return Language.objects.filter(profile=profile)

# Vista de creación para Languages
class LanguageCreateView(LoginRequiredMixin, CreateView):
    model = Language
    fields = ['name', 'level']
    template_name = 'language_form.html'
    success_url = reverse_lazy('language_list')

    def form_valid(self, form):
        form.instance.profile = get_object_or_404(Profile, user=self.request.user)
        messages.success(self.request, 'Language added successfully!')
        return super().form_valid(form)

# Vista de actualización para Languages
class LanguageUpdateView(LoginRequiredMixin, UpdateView):
    model = Language
    fields = ['name', 'level']
    template_name = 'language_form.html'
    success_url = reverse_lazy('language_list')

    def form_valid(self, form):
        messages.success(self.request, 'Language updated successfully!')
        return super().form_valid(form)

# Vista de eliminación para Languages
class LanguageDeleteView(LoginRequiredMixin, DeleteView):
    model = Language
    template_name = 'language_confirm_delete.html'
    success_url = reverse_lazy('language_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Language deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
# Vista de lista para Interests
class InterestListView(LoginRequiredMixin, ListView):
    model = Interest
    template_name = 'interest_list.html'

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return Interest.objects.filter(profile=profile)

# Vista de creación para Interests
class InterestCreateView(LoginRequiredMixin, CreateView):
    model = Interest
    fields = ['name']
    template_name = 'interest_form.html'
    success_url = reverse_lazy('interest_list')

    def form_valid(self, form):
        form.instance.profile = get_object_or_404(Profile, user=self.request.user)
        messages.success(self.request, 'Interest added successfully!')
        return super().form_valid(form)

# Vista de actualización para Interests
class InterestUpdateView(LoginRequiredMixin, UpdateView):
    model = Interest
    fields = ['name']
    template_name = 'interest_form.html'
    success_url = reverse_lazy('interest_list')

    def form_valid(self, form):
        messages.success(self.request, 'Interest updated successfully!')
        return super().form_valid(form)

# Vista de eliminación para Interests
class InterestDeleteView(LoginRequiredMixin, DeleteView):
    model = Interest
    template_name = 'interest_confirm_delete.html'
    success_url = reverse_lazy('interest_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Interest deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Vista de lista para Education
class EducationListView(LoginRequiredMixin, ListView):
    model = Education
    template_name = 'education_list.html'

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return Education.objects.filter(profile=profile)

# Vista de creación para Education
class EducationCreateView(LoginRequiredMixin, CreateView):
    model = Education
    fields = ['institution', 'degree', 'start_date', 'end_date', 'description']
    template_name = 'education_form.html'
    success_url = reverse_lazy('education_list')

    def form_valid(self, form):
        form.instance.profile = get_object_or_404(Profile, user=self.request.user)
        messages.success(self.request, 'Education added successfully!')
        return super().form_valid(form)

# Vista de actualización para Education
class EducationUpdateView(LoginRequiredMixin, UpdateView):
    model = Education
    fields = ['institution', 'degree', 'start_date', 'end_date', 'description']
    template_name = 'education_form.html'
    success_url = reverse_lazy('education_list')

    def form_valid(self, form):
        messages.success(self.request, 'Education updated successfully!')
        return super().form_valid(form)

# Vista de eliminación para Education
class EducationDeleteView(LoginRequiredMixin, DeleteView):
    model = Education
    template_name = 'education_confirm_delete.html'
    success_url = reverse_lazy('education_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Education deleted successfully!')
        return super().delete(request, *args, **kwargs)
    

# Vista de lista para Experience
class ExperienceListView(LoginRequiredMixin, ListView):
    model = Experience
    template_name = 'experience_list.html'

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return Experience.objects.filter(profile=profile)

# Vista de creación para Experience
class ExperienceCreateView(LoginRequiredMixin, CreateView):
    model = Experience
    fields = ['job_title', 'company', 'start_date', 'end_date', 'description']
    template_name = 'experience_form.html'
    success_url = reverse_lazy('experience_list')

    def form_valid(self, form):
        form.instance.profile = get_object_or_404(Profile, user=self.request.user)
        messages.success(self.request, 'Experience added successfully!')
        return super().form_valid(form)

# Vista de actualización para Experience
class ExperienceUpdateView(LoginRequiredMixin, UpdateView):
    model = Experience
    fields = ['job_title', 'company', 'start_date', 'end_date', 'description']
    template_name = 'experience_form.html'
    success_url = reverse_lazy('experience_list')

    def form_valid(self, form):
        messages.success(self.request, 'Experience updated successfully!')
        return super().form_valid(form)

# Vista de eliminación para Experience
class ExperienceDeleteView(LoginRequiredMixin, DeleteView):
    model = Experience
    template_name = 'experience_confirm_delete.html'
    success_url = reverse_lazy('experience_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Experience deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Vista de lista para Projects
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project_list.html'

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return Project.objects.filter(profile=profile)

# Vista de creación para Projects
class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['name', 'description', 'start_date', 'end_date', 'url', 'image']
    template_name = 'project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        form.instance.profile = get_object_or_404(Profile, user=self.request.user)
        messages.success(self.request, 'Project added successfully!')
        return super().form_valid(form)

# Vista de actualización para Projects
class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['name', 'description', 'start_date', 'end_date', 'url', 'image']
    template_name = 'project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        messages.success(self.request, 'Project updated successfully!')
        return super().form_valid(form)

# Vista de eliminación para Projects
class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'project_confirm_delete.html'
    success_url = reverse_lazy('project_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Project deleted successfully!')
        return super().delete(request, *args, **kwargs)