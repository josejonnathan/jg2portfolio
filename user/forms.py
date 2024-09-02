from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from curriculum.models import Profile 
from curriculum.models import Skill, Language, Interest, Education, Experience, Project


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Required. Inform a valid email address.',
        widget=forms.EmailInput(attrs={'class': 'form-control'})  # Aplicar Bootstrap aquí
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),  # Aplicar Bootstrap aquí
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar la clase 'form-control' a los campos de contraseña manualmente
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'title', 'bio', 'email', 'phone', 'address', 'website', 'linkedin', 'github', 'twitter', 'instagram', 'facebook', 'picture']
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
        }

class ProfileTemplateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['template', 'background_dark', 'htmltemplate']
        widgets = {
            'template': forms.Select(attrs={'class': 'form-control'},),
            'background_dark': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'htmltemplate': forms.Select(attrs={'class': 'form-control'}),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'level']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.NumberInput(attrs={'class': 'form-control'}),
        }