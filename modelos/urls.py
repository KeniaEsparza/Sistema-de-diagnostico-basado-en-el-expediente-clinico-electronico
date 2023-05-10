from xml.dom.minidom import Document
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    HomePageView,
    form_filtros,
    filtros,
    download_pdf,
    informationView
)

urlpatterns = [
    path('', HomePageView.as_view(), name='modelos'), #agrega un paciente
    path('filtrar/', form_filtros, name='filtrar_modelos'), #filtrar datos para diagnostico
    path('filtrar/addrecord/', filtros, name='addrecord'),
    path('filtrar/addrecord/download_my_pdf/', download_pdf, name='descarga'),
    path('informacion/', informationView.as_view(), name= 'informacion_modelos')
]