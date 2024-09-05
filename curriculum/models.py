# curriculum/models.py

from django.db import models
from django.conf import settings
from api.models import Template
from PIL import Image 
import os


class HTMLTemplate(models.Model):
    name = models.CharField(max_length=100)
    html = models.FileField(upload_to='templates')
    
    def __str__(self):
        return self.name
    

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profiles', blank=True, null=True)
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, blank=True, null=True)
    background_dark = models.BooleanField(default=False)
    htmltemplate = models.ForeignKey(HTMLTemplate, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        try:
            this = Profile.objects.get(id=self.id)
            if this.picture != self.picture and this.picture.name:
                this.picture.delete(save=False)
        except Profile.DoesNotExist:
            pass 

        super().save(*args, **kwargs)
        
        if self.picture:
            img = Image.open(self.picture.path)
            max_size = (800, 800)

            if img.height > max_size[0] or img.width > max_size[1]:
                img.thumbnail(max_size)

            dpi = (72, 72)
            img.info['dpi'] = dpi

            if img.format != 'JPEG':
                img = img.convert('RGB')  

            img.save(self.picture.path, format='JPEG', dpi=dpi, quality=85)  

    def delete(self, *args, **kwargs):
        if self.picture:
            self.picture.delete(save=False)
        super().delete(*args, **kwargs)
    
class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Language(models.Model):
    LEVEL_CHOICES = [
        ('Basic', 'Basic'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='languages')
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.level})"
    
class Interest(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='interests')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    url = models.URLField(blank=True)
    image = models.ImageField(upload_to='projects', blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si existe y es diferente de la nueva
        try:
            this = Project.objects.get(id=self.id)
            if this.image != self.image and this.image.name:
                this.image.delete(save=False)
        except Project.DoesNotExist:
            pass  # Esto es la primera vez que se guarda el objeto, por lo que no hay imagen antigua

        super().save(*args, **kwargs)
        
        if self.image:
            img = Image.open(self.image.path)
            max_size = (500, 500)

            # Redimensionar la imagen si es más grande que el tamaño máximo
            if img.height > max_size[0] or img.width > max_size[1]:
                img.thumbnail(max_size)

            # Cambiar DPI a 72
            dpi = (72, 72)
            img.info['dpi'] = dpi

            # Convertir la imagen a JPEG para optimización
            if img.format != 'JPEG':
                img = img.convert('RGB')  # Convertir a RGB si la imagen es PNG o cualquier otro formato

            img.save(self.image.path, format='JPEG', dpi=dpi, quality=85)  # Guardar como JPEG con resolución de 72 DPI y calidad de 85

    def delete(self, *args, **kwargs):
        # Eliminar la imagen cuando se elimina el objeto
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)

class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    def clean(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError(_('End date cannot be earlier than start date.'))


    def __str__(self):
        return f"{self.degree} at {self.institution}"

class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experience')
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    def clean(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError(_('End date cannot be earlier than start date.'))

    def __str__(self):
        return f"{self.job_title} at {self.company}"
    


