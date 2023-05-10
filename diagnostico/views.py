from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class HomePageView(LoginView):
    template_name = 'TrueHome.html'
    success_url = reverse_lazy('entro')#plantilla 

class EntroPageView(TemplateView):
    template_name='index.html'