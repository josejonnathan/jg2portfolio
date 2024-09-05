from django.contrib import admin
from .models import Profile, Skill, Language, Interest, Project, Education, Experience, HTMLTemplate

# Configuración personalizada para el modelo Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'email', 'phone', 'website')  # Mostrar campos relevantes en la lista

# Configuración personalizada para el modelo Skill
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'level', 'profile')  # Mostrar el ID, nombre, nivel y perfil relacionado

# Configuración personalizada para el modelo Language
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'level', 'profile')  # Mostrar el ID, nombre, nivel y perfil relacionado

# Configuración personalizada para el modelo Interest
@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'profile')  # Mostrar el ID, nombre y perfil relacionado

# Configuración personalizada para el modelo Project
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_date', 'end_date', 'profile')  # Mostrar el ID, nombre, fechas y perfil relacionado

# Configuración personalizada para el modelo Education
@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('id', 'degree', 'institution', 'start_date', 'end_date', 'profile')  # Mostrar el ID, título, institución, fechas y perfil relacionado

# Configuración personalizada para el modelo Experience
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_title', 'company', 'start_date', 'end_date', 'profile')  # Mostrar el ID, título del trabajo, compañía, fechas y perfil relacionado

# Registrar el modelo HTMLTemplate sin cambios adicionales
admin.site.register(HTMLTemplate)