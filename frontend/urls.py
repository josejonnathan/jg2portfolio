from django.urls import path
from .views import render_template_from_api

urlpatterns = [
    path('render-template/<int:template_id>/', render_template_from_api, name='render_template'),
]
