# curriculum/models.py

from django.db import models
from django.conf import settings
from api.models import Template

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

    def __str__(self):
        return self.name
    
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
