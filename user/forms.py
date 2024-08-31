from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from curriculum.models import Profile 
from curriculum.models import Skill, Language, Interest, Education, Experience, Project


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requerido. Introduzca una dirección de correo electrónico válida.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'title', 'bio', 'email', 'phone', 'address', 'website', 'linkedin', 'github', 'twitter', 'instagram', 'facebook', 'picture', 'template', 'background_dark', 'htmltemplate']
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
            'template': forms.Select(attrs={'class': 'form-control'}),
            'background_dark': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'htmltemplate': forms.Select(attrs={'class': 'form-control'}),
        }