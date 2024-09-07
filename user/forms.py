from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from curriculum.models import Profile, Skill, Language, Interest, Education, Experience, Project
from django.core.exceptions import ValidationError
from PIL import Image
from user.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text=_('Required. Enter a valid email address.'),
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label=_('I accept the terms and conditions')
    )

    class Meta:
        model = CustomUser  # Usar el modelo de usuario personalizado
        fields = ('username', 'email', 'password1', 'password2', 'terms')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': _('Username'),
            'email': _('Email'),
            'password1': _('Password'),
            'password2': _('Confirm Password'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'name', 'title', 'bio', 'email', 'phone', 'address', 'website', 'linkedin',
            'github', 'twitter', 'instagram', 'facebook', 'picture', 'password_protected', 'password'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'github': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'password_protected': forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # Checkbox para habilitar protección por contraseña
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),  # Campo de contraseña
        }
        labels = {
            'name': _('Name'),
            'title': _('Title'),
            'bio': _('Bio'),
            'email': _('Email'),
            'phone': _('Phone'),
            'address': _('Address'),
            'website': _('Website'),
            'linkedin': _('LinkedIn'),
            'github': _('GitHub'),
            'twitter': _('Twitter'),
            'instagram': _('Instagram'),
            'facebook': _('Facebook'),
            'picture': _('Profile Picture'),
            'password_protected': _('Protect curriculum with password'),
            'password': _('Password'),
        }
 
    def clean_picture(self):
        picture = self.cleaned_data.get('picture', False)
        
        if picture:
            # Validar el tamaño del archivo de la imagen
            if picture.size > 5 * 1024 * 1024:  # 5 MB
                raise ValidationError(_("The image is too large (maximum size is 5 MB)."))

            # Validar las dimensiones de la imagen
            max_width, max_height = 5000, 5000  # Límites máximos de dimensiones de imagen
            img = Image.open(picture)
            if img.width > max_width or img.height > max_height:
                raise ValidationError(_(f"Image Resolution is too high (maximum size is {max_width}x{max_height} pixels)."))

        return picture

    def clean(self):
        cleaned_data = super().clean()
        password_protected = cleaned_data.get("password_protected")
        password = cleaned_data.get("password")

        if password_protected and not password:
            raise ValidationError(_("You must provide a password if password protection is enabled."))

        return cleaned_data


class ProfileTemplateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['background_dark', 'htmltemplate']
        widgets = {
            'background_dark': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'htmltemplate': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'background_dark': _('Dark Background'),  # Etiqueta de traducción añadida
            'htmltemplate': _('Template'),  # Etiqueta de traducción añadida
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'level']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'level': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required', 'min': 1, 'max': 100}),
        }
        labels = {
            'name': _('Skill Name'),
            'level': _('Skill Level'),
        }
        error_messages = {
            'name': {
                'required': _('Please enter the skill name'),
            },
            'level': {
                'required': _('Please enter the skill level'),
                'min_value': _('Minimum level is 1'),
                'max_value': _('Maximum level is 100'),
            },
        }

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name', 'level']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}), 
        }
        labels = {
            'name': _('Language Name'),  # Etiqueta de traducción añadida
            'level': _('Proficiency Level'),  # Etiqueta de traducción añadida
        }

class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': _('Interest'),  # Etiqueta de traducción añadida
        }

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'start_date', 'end_date', 'description']
        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'institution': _('Institution'),  # Etiqueta de traducción añadida
            'degree': _('Degree'),  # Etiqueta de traducción añadida
            'start_date': _('Start Date'),  # Etiqueta de traducción añadida
            'end_date': _('End Date'),  # Etiqueta de traducción añadida
            'description': _('Description'),  # Etiqueta de traducción añadida
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.instance and self.instance.pk:
                self.fields['start_date'].initial = self.instance.start_date.strftime('%Y-%m-%d') if self.instance.start_date else ''
                self.fields['end_date'].initial = self.instance.end_date.strftime('%Y-%m-%d') if self.instance.end_date else ''

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['job_title', 'company', 'start_date', 'end_date', 'description']
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'job_title': _('Job Title'),  # Etiqueta de traducción añadida
            'company': _('Company'),  # Etiqueta de traducción añadida
            'start_date': _('Start Date'),  # Etiqueta de traducción añadida
            'end_date': _('End Date'),  # Etiqueta de traducción añadida
            'description': _('Description'),  # Etiqueta de traducción añadida
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.instance and self.instance.pk:
                self.fields['start_date'].initial = self.instance.start_date.strftime('%Y-%m-%d') if self.instance.start_date else ''
                self.fields['end_date'].initial = self.instance.end_date.strftime('%Y-%m-%d') if self.instance.end_date else ''

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'url', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': _('Project Name'),
            'description': _('Description'),
            'start_date': _('Start Date'),
            'end_date': _('End Date'),
            'url': _('Project URL'),
            'image': _('Project Image'),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.instance and self.instance.pk:
                self.fields['start_date'].initial = self.instance.start_date.strftime('%Y-%m-%d') if self.instance.start_date else ''
                self.fields['end_date'].initial = self.instance.end_date.strftime('%Y-%m-%d') if self.instance.end_date else ''

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        
        if image:
            # Validar el tamaño del archivo de la imagen
            if image.size > 5 * 1024 * 1024:  # 5 MB
                raise ValidationError(_("The image is too large (maximum size is 5 MB)."))

            # Validar las dimensiones de la imagen
            max_width, max_height = 5000, 5000  # Límites máximos de dimensiones de imagen
            img = Image.open(image)
            if img.width > max_width or img.height > max_height:
                raise ValidationError(_(f"Image Resolution is too high (maximum size is {max_width}x{max_height} pixels)."))

        return image
