from xml.dom.minidom import Document
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    filtros,
    res_graficos
)

urlpatterns = [
    path('', filtros, name='estadisticas'), #agrega un paciente
    path('addrecord/', res_graficos, name='addrecord'),
]