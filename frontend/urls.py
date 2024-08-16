from django.urls import path
from .views import home_view, egg_view

urlpatterns = [
    path('', home_view, name='home'), 
    path('egg/', egg_view, name='egg'),
]
