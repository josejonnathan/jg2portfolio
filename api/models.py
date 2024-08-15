from django.db import models


class HeroImage(models.Model):
    title = models.CharField(max_length=200, help_text="Hero image title")
    image = models.ImageField(upload_to='hero_images/', help_text="Hero image")
    alt_text = models.CharField(max_length=200, help_text="Alternative text", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Colors(models.Model):
    name = models.CharField(max_length=100, help_text="Descriptive name for the color scheme")
    primary = models.CharField(max_length=7, help_text="Primary color in hexadecimal format", default="#000000")
    secondary = models.CharField(max_length=7, help_text="Secondary color in hexadecimal format", default="#000000")
    tertiary = models.CharField(max_length=7, help_text="Tertiary color in hexadecimal format", default="#000000")
    light = models.CharField(max_length=7, help_text="Light color in hexadecimal format", default="#FFFFFF")
    dark = models.CharField(max_length=7, help_text="Dark color in hexadecimal format", default="#000000")

    def __str__(self):
        return self.name
    

class Template(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the template")
    colors = models.ForeignKey(Colors, on_delete=models.SET_NULL, null=True, blank=True, help_text="Color scheme for the template")
    hero_image = models.ForeignKey(HeroImage, on_delete=models.SET_NULL, null=True, blank=True, help_text="Hero image for the template")
    active = models.BooleanField(default=True, help_text="Indicates if this template is active")

    def __str__(self):
        return self.name
    

class Project(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the project")
    description = models.TextField(help_text="Description of the project")
    url = models.URLField(max_length=200, help_text="URL of the project")
    image = models.ImageField(upload_to='proyectos/', help_text="Image of the project")
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    order = models.IntegerField(help_text="Order of the project in the list", default=0)

    def __str__(self):
        return self.name
    



