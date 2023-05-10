from pickle import OBJ
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.text import capfirst
from django.contrib.auth.models import AbstractUser

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.core.exceptions import PermissionDenied # checa que el usuario sea el mismo que comento

from users.forms import CustomUserChangeForm, CustomUserCreationForm, BasicCreationForm
from django.views.generic import TemplateView
from .forms import CustomUser
from django.db.models import Q

class DoctoresPageView(TemplateView):
    template_name = 'doctores.html'

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')#plantilla
    template_name = 'signup.html'

    def dispatch(self, form): #permiso
        if self.request.user.is_superuser:
            return super().dispatch(form)
        return redirect('error') 

class SignUpBasicView(CreateView):
    form_class = BasicCreationForm
    success_url = reverse_lazy('entro')#plantilla
    template_name = 'basic.html'

    """ def dispatch(self, form): #permiso
        if self.request.user.is_authenticated:
            return super().dispatch(form)
        return redirect('error')  """
        

class EditView(UpdateView): #actualizar/editar
    model = CustomUser
    fields =('username', 'email', 'nombre', 'apellido', 'is_superuser')
    template_name = 'edit.html'
    login_url = 'login'
    success_url = reverse_lazy('entro')#plantilla

class EditBasicView(UpdateView): #actualizar/editar
    model = CustomUser
    fields =('username', 'email', 'nombre', 'apellido')
    template_name = 'edit_basic.html'
    login_url = 'login'
    success_url = reverse_lazy('entro')#plantilla

class ErrorView(TemplateView):
    template_name = 'not-found.html'

class UserListView(ListView):#lista de articulos
    model = CustomUser
    template_name = 'user_list.html'
    login_url = 'home'

    """ def dispatch(self, form): #permiso
        if self.request.user.is_superuser:
            return super().dispatch(form)
        return redirect('error')  """

class UserDeleteView(DeleteView): #borrar
    model = CustomUser
    template_name = 'user_delete.html'
    login_url = 'login'  
    success_url = reverse_lazy('entro')#plantilla  

#Buscar user
class SearchUserListView(ListView):
    model = CustomUser
    context_object_paciente = 'object_list'
    template_name = 'user_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return CustomUser.objects.filter(
            Q(username__icontains = query)
        )