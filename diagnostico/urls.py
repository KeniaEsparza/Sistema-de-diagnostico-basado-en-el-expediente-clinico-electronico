"""diagnostico URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import HomePageView, EntroPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('admin/defender/',include('defender.urls')), #defender admin
    path('', HomePageView.as_view(), name='home'),
    path('entro/', EntroPageView.as_view(), name='entro'),
    path('users/', include('users.urls')), #app de usuarios
    path('users/', include('django.contrib.auth.urls')), # app de usuarios(django)
    path('pacientes/', include('paciente.urls')), #app de usuarios
    path('modelos/', include('modelos.urls')), #app de modelos
    path('estadisticas/', include('estadisticas.urls')), #app de estadisticas
]
