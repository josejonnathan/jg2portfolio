from rest_framework import serializers
from .models import HeroImage, Colors, Template, Project

class HeroImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroImage
        fields = ['id', 'title', 'image', 'alt_text', 'created_at']

class ColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colors
        fields = ['id', 'name', 'primary', 'secondary', 'tertiary', 'light', 'dark']

class TemplateSerializer(serializers.ModelSerializer):
    colors = ColorsSerializer(read_only=True)
    hero_image = HeroImageSerializer(read_only=True)

    class Meta:
        model = Template
        fields = ['id', 'name', 'html_file', 'colors', 'hero_image', 'active']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'url', 'image', 'creation_date', 'update_date']