from contextvars import Context
from math import floor
from unittest import result
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from matplotlib.style import context
from datetime import datetime
from requests import request # Autorizacion
from .forms import LabortorioForm
from django import forms
from django.core.files.storage import FileSystemStorage

from paciente.models import Nota_inicial, Paciente, Nota_egreso, Pruebas_especiales, Quimica_clinica, Medicina_nuclear,Laboratorio,Inmunologia,Inmuno_infecto,Hematologia,Drogas_terapeuticas,Coagulaciones
from django.db.models import Q
import os
import PyPDF2
from os import remove

from django.contrib import messages
import Funciones.backup as backup

class HomePageView(TemplateView):
    template_name = 'paciente.html'

#Crear paciente
class PacienteCreateView(LoginRequiredMixin, CreateView):
    model = Paciente
    template_name = 'nuevo_paciente.html'
    fields = ('nss',)
    login_url = 'login'
    success_url = reverse_lazy('pacientes')#plantilla 

    def dispatch(self, form): #permiso para autentificados
        if self.request.user.is_authenticated:
            return super().dispatch(form)
        return redirect('error') 

#Crear nota inicial
class Nota_inicialCreateView(CreateView):
    model = Nota_inicial
    template_name = 'nueva_nota_inicial.html'
    fields = ('fecha_ingreso','genero','especialidad_ingreso','motivo_inter','interrogatorio','dx','plan_tratamiento','pronostico',
        'indicaciones','estado_salud','peso','talla','temperatura','frec_respiratoria','frec_cardiaca','pres_arterial','imc','saturacion','glc_capilar',
        'diagnostico_inicial',)
    success_url = reverse_lazy('pacientes')#plantilla 

    def form_valid(self, form):#funcion para agregar paarmetros a los formularios
        form.instance.nss = self.kwargs['pk']
        return super ().form_valid(form) 

#Crear Nota_inicial
def Nota_inicialCreateView(request,nss):
    template = loader.get_template('nueva_nota_inicial.html')
    context = {'nss' : nss}
    return HttpResponse(template.render(context,request))

def addrecordnotainicial(request, nss):
    fecha_ingreso = request.POST['fecha_ingreso']
    genero = request.POST['genero']
    especialidad_ingreso = request.POST['especialidad_ingreso']
    motivo_inter = request.POST['motivo_inter']
    interrogatorio = request.POST['interrogatorio']
    dx = request.POST['dx']
    plan_tratamiento = request.POST['plan_tratamiento']
    pronostico = request.POST['pronostico']
    indicaciones = request.POST['indicaciones']
    estado_salud = request.POST['estado_salud']
    peso = request.POST['peso']
    talla = request.POST['talla']
    temperatura = request.POST['temperatura']
    frec_respiratoria = request.POST['frec_respiratoria']
    frec_cardiaca = request.POST['frec_cardiaca']
    pres_arterial = request.POST['pres_arterial']
    imc = request.POST['imc']
    saturacion = request.POST['saturacion']
    glc_capilar = request.POST['glc_capilar']
    diagnostico_inicial = request.POST['diagnostico_inicial']

    nota = Nota_inicial(
        nss = nss,
        fecha_ingreso = fecha_ingreso,
        genero = genero,
        especialidad_ingreso = especialidad_ingreso,
        motivo_inter = motivo_inter,
        interrogatorio = interrogatorio,
        dx = dx,
        plan_tratamiento = plan_tratamiento,
        pronostico = pronostico,
        indicaciones = indicaciones,
        estado_salud = estado_salud,
        peso = peso,
        talla = talla,
        temperatura = temperatura,
        frec_respiratoria = frec_respiratoria,
        frec_cardiaca = frec_cardiaca,
        pres_arterial = pres_arterial,
        imc = imc,
        saturacion = saturacion,
        glc_capilar = glc_capilar,
        diagnostico_inicial = diagnostico_inicial,
    )
    nota.save(force_insert=True)
    backup.backup()
    return HttpResponseRedirect(reverse('pacientes')) 

#Crear Nota_egreso
def Nota_egresoCreateView(request,nss):
    template = loader.get_template('nueva_nota_egreso.html')
    context = {'nss' : nss}
    return HttpResponse(template.render(context,request))

def addrecordnotaegreso(request, nss):
    fecha_ingreso = request.POST['fecha_ingreso']
    fecha_egreso = request.POST['fecha_egreso']
    especialidad_egreso = request.POST['especialidad_egreso']
    motivo_egreso = request.POST['motivo_egreso']
    envio = request.POST['envio']
    diagnostico_ingreso = request.POST['diagnostico_ingreso']
    diagnostico_egreso = request.POST['diagnostico_egreso']
    resumen_evolucion = request.POST['resumen_evolucion']
    problemas_pendientes = request.POST['problemas_pendientes']
    plan_tratamiento = request.POST['plan_tratamiento']
    recomendaciones = request.POST['recomendaciones']
    factores_riesgo = request.POST['factores_riesgo']
    pronostico = request.POST['pronostico']
    diagnostico_defuncion = request.POST['diagnostico_defuncion']
    estado_salud = request.POST['estado_salud']
    peso = request.POST['peso']
    talla = request.POST['talla']
    temperatura = request.POST['temperatura']
    frec_respiratoria = request.POST['frec_respiratoria']
    frec_cardiaca = request.POST['frec_cardiaca']
    pres_arterial = request.POST['pres_arterial']
    imc = request.POST['imc']
    saturacion = request.POST['saturacion']
    glc_capilar = request.POST['glc_capilar']
    diagnostico_final = request.POST['diagnostico_final']

    nota = Nota_egreso(
        nss = nss,
        fecha_ingreso = fecha_ingreso,
        fecha_egreso = fecha_egreso,
        especialidad_egreso = especialidad_egreso,
        motivo_egreso = motivo_egreso,
        envio = envio,
        diagnostico_ingreso = diagnostico_ingreso,
        diagnostico_egreso = diagnostico_egreso,
        resumen_evolucion = resumen_evolucion,
        problemas_pendientes = problemas_pendientes,
        plan_tratamiento = plan_tratamiento,
        recomendaciones = recomendaciones,
        factores_riesgo = factores_riesgo,
        pronostico = pronostico,
        diagnostico_defuncion = diagnostico_defuncion,
        estado_salud = estado_salud,
        peso = peso,
        talla = talla,
        temperatura = temperatura,
        frec_respiratoria = frec_respiratoria,
        frec_cardiaca = frec_cardiaca,
        pres_arterial = pres_arterial,
        imc = imc,
        saturacion = saturacion,
        glc_capilar = glc_capilar,
        diagnostico_final = diagnostico_final,
    )
    nota.save(force_insert=True)
    backup.backup()
    return HttpResponseRedirect(reverse('pacientes'))

#Crear Pruebas_especiales
def Pruebas_especialesCreateView(request,nss):
    template = loader.get_template('nueva_pruebas_especiales.html')
    context = {'nss' : nss}
    return HttpResponse(template.render(context,request))

def addrecordpruebasespeciales(request, nss):
    folio_orden = request.POST['folio_orden']
    determinacion = request.POST['determinacion']
    resultado = request.POST['resultado']
    unidad = request.POST['unidad']
    valor_normal = request.POST['valor_normal']

    nota = Pruebas_especiales(
        nss = nss,
        folio_orden = folio_orden,
        determinacion = determinacion,
        resultado = resultado,
        unidad = unidad,
        valor_normal = valor_normal,
    )
    nota.save(force_insert=True)
    backup.backup()
    return HttpResponseRedirect(reverse('pacientes'))

#Crear Quimica_clinica
def Quimica_clinicaCreateView(request,nss):
    template = loader.get_template('nueva_quimica_clinica.html')
    context = {'nss' : nss}
    return HttpResponse(template.render(context,request))

def addrecordquimicaclinica(request, nss):
    folio_orden = request.POST['folio_orden']
    determinacion = request.POST['determinacion']
    resultado = request.POST['resultado']
    unidad = request.POST['unidad']
    valor_normal = request.POST['valor_normal']

    nota = Quimica_clinica(
        nss = nss,
        folio_orden = folio_orden,
        determinacion = determinacion,
        resultado = resultado,
        unidad = unidad,
        valor_normal = valor_normal,
    )
    nota.save(force_insert=True)
    backup.backup()
    return HttpResponseRedirect(reverse('pacientes')) 

#Crear Medicina_nuclear
def Medicina_nuclearCreateView(request,nss):
    template = loader.get_template('nueva_medicina_nuclear.html')
    context = {'nss' : nss}
    return HttpResponse(template.render(context,request))

def addrecordmedicinanuclear(request, nss):
    folio_orden = request.POST['folio_orden']
    determinacion = request.POST['determinacion']
    resultado = request.POST['resultado']
    unidad = request.POST['unidad']
    valor_normal = request.POST['valor_normal']

    nota = Medicina_nuclear(
        nss = nss,
        folio_orden = folio_orden,
        determinacion = determinacion,
        resultado = resultado,
        unidad = unidad,
        valor_normal = valor_normal,
    )
    nota.save(force_insert=True)
    backup.backup()
    return HttpResponseRedirect(reverse('pacientes'))

#Crear Laboratorio
def LaboratorioCreateView(request,nss):
    template = loader.get_template('nuevo_laboratorio.html')
    context = {'nss' : nss}
    return HttpResponse(template.render(context,request))

def addrecordlaboratorio(request, nss):
    folio_orden = request.POST['folio_orden']
    fecha_orden = request.POST['fecha_orden']
    edad = request.POST['edad']
    servicio_solicita = request.POST['servicio_solicita']

    nota = Laboratorio(
        nss = nss,
        folio_orden = folio_orden,
        fecha_orden = fecha_orden,
        edad = edad,
        servicio_solicita = servicio_solicita,
    )
    nota.save(force_insert=True)
    backup.backup()
    return HttpResponseRedirect(reverse('pacientes'))

#Crear Inmunologia
def InmunologiaCreateView(request,nss):
    template = loader.get_template('nuevo_inmunologia.html')
    context = {'nss' : nss}
    return HttpResponse(template.render(context,request))

def addrecordInmunologia(request, nss):
    folio_orden = request.POST['folio_orden']
    determinacion = request.POST['determinacion']
    resultado = request.POST['resultado']
    unidad = request.POST['unidad']
    valor_normal = request.POST['valor_normal']

    nota = Inmunologia(
        nss = nss,
        folio_orden = folio_orden,
        determinacion = determinacion,
        resultado = resultado,
        unidad = unidad,
        valor_normal = valor_normal,
    )
    nota.save(force_insert=True)
    backup.backup()
    return HttpResponseRedirect(reverse('pacientes'))

#Crear Inmuno_infecto
def Inmuno_infectoCreateView(request,nss):
    template = loader.get_template('nuevo_infecto.html')
    context = {'nss' : nss}
    return HttpResponse(template.render(context,request))

def addrecordinmunoinfecto(request, nss):
    folio_orden = request.POST['folio_orden']
    determinacion = request.POST['determinacion']
    resultado = request.POST['resultado']
    unidad = request.POST['unidad']
    valor_normal = request.POST['valor_normal']

    nota = Inmuno_infecto(
        nss = nss,
        folio_orden = folio_orden,
        determinacion = determinacion,
        resultado = resultado,
        unidad = unidad,
        valor_normal = valor_normal,
    )
    nota.save(force_insert=True)
    backup.backup()
    return HttpResponseRedirect(reverse('pacientes'))

#Crear Inmuno_infecto
def Inmuno_infectoCreateView(request,nss):
    template = loader.get_template('nuevo_infecto.html')
    context = {'nss' : nss}
    return HttpResponse(template.render(context,request))

def addrecordinmunoinfecto(request, nss):
    folio_orden = request.POST['folio_orden']
    determinacion = request.POST['determinacion']
    resultado = request.POST['resultado']
    unidad = request.POST['unidad']
    valor_normal = request.POST['valor_normal']

    nota = Inmuno_infecto(
        nss = nss,
        folio_orden = folio_orden,
        determinacion = determinacion,
        resultado = resultado,
        unidad = unidad,
        valor_normal = valor_normal,
    )
    nota.save(force_insert=True)
    backup.backup()
    return HttpResponseRedirect(reverse('pacientes'))

#Crear Hematologia
def HematologiaCreateView(request,nss):
    template = loader.get_template('nuevo_hematologia.html')
    context = {'nss' : nss}
    return HttpResponse(template.render(context,request))

def addrecordhematologia(request, nss):
    folio_orden = request.POST['folio_orden']
    determinacion = request.POST['determinacion']
    resultado = request.POST['resultado']
    unidad = request.POST['unidad']
    valor_normal = request.POST['valor_normal']

    nota = Hematologia(
        nss = nss,
        folio_orden = folio_orden,
        determinacion = determinacion,
        resultado = resultado,
        unidad = unidad,
        valor_normal = valor_normal,
    )
    nota.save(force_insert=True)
    backup.backup()
    return HttpResponseRedirect(reverse('pacientes')) 

#Crear Drogas_terapeuticas
def Drogas_terapeuticasCreateView(request,nss):
    template = loader.get_template('nuevo_drogas_terapeuticas.html')
    context = {'nss' : nss}
    return HttpResponse(template.render(context,request))

def addrecorddrogasterapeuticas(request, nss):
    folio_orden = request.POST['folio_orden']
    determinacion = request.POST['determinacion']
    resultado = request.POST['resultado']
    unidad = request.POST['unidad']
    valor_normal = request.POST['valor_normal']

    nota = Drogas_terapeuticas(
        nss = nss,
        folio_orden = folio_orden,
        determinacion = determinacion,
        resultado = resultado,
        unidad = unidad,
        valor_normal = valor_normal,
    )
    nota.save(force_insert=True)
    backup.backup()
    return HttpResponseRedirect(reverse('pacientes')) 

#Crear Coagulaciones
def CoagulacionesCreateView(request,nss):
    template = loader.get_template('nuevo_coagulaciones.html')
    context = {'nss' : nss}
    return HttpResponse(template.render(context,request))

def addrecordcoagulaciones(request, nss):
    folio_orden = request.POST['folio_orden']
    determinacion = request.POST['determinacion']
    resultado = request.POST['resultado']
    unidad = request.POST['unidad']
    valor_normal = request.POST['valor_normal']

    nota = Coagulaciones(
        nss = nss,
        folio_orden = folio_orden,
        determinacion = determinacion,
        resultado = resultado,
        unidad = unidad,
        valor_normal = valor_normal,
    )
    nota.save(force_insert=True)
    backup.backup()
    return HttpResponseRedirect(reverse('pacientes')) 

#Buscar paciente
class SearchPacienteListView(ListView):
    model = Paciente
    context_object_paciente = 'paciente_list'
    template_name = 'search_paciente.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Paciente.objects.filter(
            Q(nss__icontains = query) | Q(nombre_paciente__icontains = query)
        )
    def dispatch(self, form): #permiso para autentificados
        if self.request.user.is_authenticated:
            return super().dispatch(form)
        return redirect('error') 

class PacienteDetailView(DetailView): #detalles
    model = Paciente
    template_name = 'paciente_detail.html'
    login_url = 'login'

#Buscar nota_inicial
class SearchNotaInicialListView(ListView):
    model = Nota_inicial
    context_object_nota_inicial = 'nota_inicial_list'
    template_name = 'search_nota_inicial.html'

    def get_queryset(self):
        query = float(self.kwargs['pk'])
        query = floor(query)
        return Nota_inicial.objects.filter(
            Q(nss__icontains = query)
        )

#Buscar nota_inicial
class SearchNotaEgresoListView(ListView):
    model = Nota_egreso
    context_object_nota_inicial = 'nota_egreso_list'
    template_name = 'search_nota_egreso.html'

    def get_queryset(self):
        query = float(self.kwargs['pk'])
        query = floor(query)
        return Nota_egreso.objects.filter(
            Q(nss__icontains = query)
        )

#Buscar Pruebas_especiales
class SearchPruebasEspecialesListView(ListView):
    model = Pruebas_especiales
    context_object_nota_inicial = 'pruebas_especiales_list'
    template_name = 'search_pruebas_especiales.html'

    def get_queryset(self):
        query = float(self.kwargs['pk'])
        query = floor(query)
        return Pruebas_especiales.objects.filter(
            Q(nss__icontains = query)
        )

#Buscar Quimica_clinica
class SearchQuimicaclinicaListView(ListView):
    model = Quimica_clinica
    context_object_nota_inicial = 'quimica_clinica_list'
    template_name = 'search_quimica_clinica.html'

    def get_queryset(self):
        query = float(self.kwargs['pk'])
        query = floor(query)
        return Quimica_clinica.objects.filter(
            Q(nss__icontains = query)
        )

#Buscar Medicina_nuclear
class SearcMedicinanuclearListView(ListView):
    model = Medicina_nuclear
    context_object_nota_inicial = 'medicina_nuclear_list'
    template_name = 'search_medicina_nuclear.html'

    def get_queryset(self):
        query = float(self.kwargs['pk'])
        query = floor(query)
        return Medicina_nuclear.objects.filter(
            Q(nss__icontains = query)
        )

#Buscar Laboratorio
class SearcLaboratorioListView(ListView):
    model = Laboratorio
    context_object_nota_inicial = 'laboratorio_list'
    template_name = 'search_laboratorio.html'

    def get_queryset(self):
        query = float(self.kwargs['pk'])
        query = floor(query)
        return Laboratorio.objects.filter(
            Q(nss__icontains = query)
        )

#Buscar Inmunologia
class SearcInmunologiaListView(ListView):
    model = Inmunologia
    context_object_nota_inicial = 'inmunologia_list'
    template_name = 'search_inmunologia.html'

    def get_queryset(self):
        query = float(self.kwargs['pk'])
        query = floor(query)
        return Inmunologia.objects.filter(
            Q(nss__icontains = query)
        )

#Buscar Inmuno_infecto
class SearcinmunoinfectoListView(ListView):
    model = Inmuno_infecto
    context_object_nota_inicial = 'inmuno_infecto_list'
    template_name = 'search_inmuno_infecto.html'

    def get_queryset(self):
        query = float(self.kwargs['pk'])
        query = floor(query)
        return Inmuno_infecto.objects.filter(
            Q(nss__icontains = query)
        )

#Buscar Hematologia
class SearchematologiaListView(ListView):
    model = Hematologia
    context_object_nota_inicial = 'hematologia_list'
    template_name = 'search_hematologia.html'

    def get_queryset(self):
        query = float(self.kwargs['pk'])
        query = floor(query)
        return Hematologia.objects.filter(
            Q(nss__icontains = query)
        )

#Buscar Drogas_terapeuticas
class SearchdrogasterapeuticasListView(ListView):
    model = Drogas_terapeuticas
    context_object_nota_inicial = 'drogas_terapeuticas_list'
    template_name = 'search_drogas_terapeuticas.html'

    def get_queryset(self):
        query = float(self.kwargs['pk'])
        query = floor(query)
        return Drogas_terapeuticas.objects.filter(
            Q(nss__icontains = query)
        )

#Buscar Coagulaciones
class SearchcoagulacionesListView(ListView):
    model = Coagulaciones
    context_object_nota_inicial = 'coagulaciones_list'
    template_name = 'search_coagulaciones.html'

    def get_queryset(self):
        query = float(self.kwargs['pk'])
        query = floor(query)
        return Coagulaciones.objects.filter(
            Q(nss__icontains = query)
        )

class Nota_inicialDetailView(ListView): #detalles
    model = Nota_inicial
    context_object_paciente = 'nota_inicial_list'
    template_name = 'Nota_inicial.html'

    def get_queryset(self):
        query = self.request.GET.get('nss')
        query = query[:-2] 
        query2 = self.request.GET.get('fecha_ingreso')
        fecha = str(query2)
        fecha = fecha.replace(' de ', ' ')
        fecha = fecha.replace('enero', '01')
        fecha = fecha.replace('febrero', '02')
        fecha = fecha.replace('marzo', '03')
        fecha = fecha.replace('abril', '04')
        fecha = fecha.replace('mayo', '05')
        fecha = fecha.replace('junio', '06')
        fecha = fecha.replace('julio', '07')
        fecha = fecha.replace('agosto', '08')
        fecha = fecha.replace('septiembre', '09')
        fecha = fecha.replace('octubre', '10')
        fecha = fecha.replace('noviembre', '11')
        fecha = fecha.replace('diciembre', '12')
        fecha = fecha.replace(' ', '-')
        fecha = datetime.strptime(fecha, '%d-%m-%Y')
        fecha = fecha.strftime('%Y-%m-%d')
        return Nota_inicial.objects.filter(
            Q(nss__icontains = query) & Q(fecha_ingreso__icontains = fecha) 
        )

class Nota_egresoDetailView(ListView): #detalles
    model = Nota_egreso
    context_object_paciente = 'nota_egreso_list'
    template_name = 'Nota_egreso.html'

    def get_queryset(self):
        query = self.request.GET.get('nss')
        query = query[:-2] 
        query2 = self.request.GET.get('fecha_egreso')
        fecha = str(query2)
        fecha = fecha.replace(' de ', ' ')
        fecha = fecha.replace('enero', '01')
        fecha = fecha.replace('febrero', '02')
        fecha = fecha.replace('marzo', '03')
        fecha = fecha.replace('abril', '04')
        fecha = fecha.replace('mayo', '05')
        fecha = fecha.replace('junio', '06')
        fecha = fecha.replace('julio', '07')
        fecha = fecha.replace('agosto', '08')
        fecha = fecha.replace('septiembre', '09')
        fecha = fecha.replace('octubre', '10')
        fecha = fecha.replace('noviembre', '11')
        fecha = fecha.replace('diciembre', '12')
        fecha = fecha.replace(' ', '-')
        fecha = datetime.strptime(fecha, '%d-%m-%Y')
        fecha = fecha.strftime('%Y-%m-%d')
        return Nota_egreso.objects.filter(
            Q(nss__icontains = query) & Q(fecha_egreso__icontains = fecha) 
        )

class Pruebas_especialesDetailView(ListView): #detalles
    model = Pruebas_especiales
    context_object_paciente = 'pruebas_especiales_list'
    template_name = 'Pruebas_especiales.html'

    def get_queryset(self):
        query = self.request.GET.get('nss')
        query = query[:-2] 
        query2 = self.request.GET.get('folio_orden')
        query2 = query2[:-2] 
        query3 = self.request.GET.get('determinacion')
        return Pruebas_especiales.objects.filter(
            Q(nss__icontains = query) & Q(folio_orden__icontains = query2) & Q(determinacion__icontains = query3)
        )

class Quimica_clinicaDetailView(ListView): #detalles
    model = Quimica_clinica
    context_object_paciente = 'quimica_clinica_list'
    template_name = 'Quimica_clinica.html'

    def get_queryset(self):
        query = self.request.GET.get('nss')
        query = query[:-2] 
        query2 = self.request.GET.get('folio_orden')
        query2 = query2[:-2] 
        query3 = self.request.GET.get('determinacion')
        return Quimica_clinica.objects.filter(
            Q(nss__icontains = query) & Q(folio_orden__icontains = query2) & Q(determinacion__icontains = query3)
        )

class Medicina_nuclearDetailView(ListView): #detalles
    model = Medicina_nuclear
    context_object_paciente = 'medicina_nuclear_list'
    template_name = 'Medicina_nuclear.html'

    def get_queryset(self):
        query = self.request.GET.get('nss')
        query = query[:-2] 
        query2 = self.request.GET.get('folio_orden')
        query2 = query2[:-2] 
        query3 = self.request.GET.get('determinacion')
        return Medicina_nuclear.objects.filter(
            Q(nss__icontains = query) & Q(folio_orden__icontains = query2) & Q(determinacion__icontains = query3)
        )

class LaboratorioDetailView(ListView): #detalles
    model = Laboratorio
    context_object_paciente = 'laboratorio_list'
    template_name = 'laboratorio.html'

    def get_queryset(self):
        query = self.request.GET.get('nss')
        query = query[:-2] 
        query2 = self.request.GET.get('folio_orden')
        query2 = query2[:-2] 
        return Laboratorio.objects.filter(
            Q(nss__icontains = query) & Q(folio_orden__icontains = query2)
        )

class InmunologiaDetailView(ListView): #detalles
    model = Inmunologia
    context_object_paciente = 'inmunologia_list'
    template_name = 'Inmunologia.html'

    def get_queryset(self):
        query = self.request.GET.get('nss')
        query = query[:-2] 
        query2 = self.request.GET.get('folio_orden')
        query2 = query2[:-2] 
        query3 = self.request.GET.get('determinacion')
        return Inmunologia.objects.filter(
            Q(nss__icontains = query) & Q(folio_orden__icontains = query2) & Q(determinacion__icontains = query3)
        )

class Inmuno_infectoDetailView(ListView): #detalles
    model = Inmuno_infecto
    context_object_paciente = 'inmuno_infecto_list'
    template_name = 'Inmuno_infecto.html'

    def get_queryset(self):
        query = self.request.GET.get('nss')
        query = query[:-2] 
        query2 = self.request.GET.get('folio_orden')
        query2 = query2[:-2] 
        query3 = self.request.GET.get('determinacion')
        return Inmuno_infecto.objects.filter(
            Q(nss__icontains = query) & Q(folio_orden__icontains = query2) & Q(determinacion__icontains = query3)
        )

class HematologiaDetailView(ListView): #detalles
    model = Hematologia
    context_object_paciente = 'hematologia_list'
    template_name = 'Hematologia.html'

    def get_queryset(self):
        query = self.request.GET.get('nss')
        query = query[:-2] 
        query2 = self.request.GET.get('folio_orden')
        query2 = query2[:-2] 
        query3 = self.request.GET.get('determinacion')
        return Hematologia.objects.filter(
            Q(nss__icontains = query) & Q(folio_orden__icontains = query2) & Q(determinacion__icontains = query3)
        )

class Drogas_terapeuticasDetailView(ListView): #detalles
    model = Drogas_terapeuticas
    context_object_paciente = 'drogas_terapeuticas_list'
    template_name = 'Drogas_terapeuticas.html'

    def get_queryset(self):
        query = self.request.GET.get('nss')
        query = query[:-2] 
        query2 = self.request.GET.get('folio_orden')
        query2 = query2[:-2] 
        query3 = self.request.GET.get('determinacion')
        return Drogas_terapeuticas.objects.filter(
            Q(nss__icontains = query) & Q(folio_orden__icontains = query2) & Q(determinacion__icontains = query3)
        )

class CoagulacionesDetailView(ListView): #detalles
    model = Coagulaciones
    context_object_paciente = 'coagulaciones_list'
    template_name = 'Coagulaciones.html'

    def get_queryset(self):
        query = self.request.GET.get('nss')
        query = query[:-2] 
        query2 = self.request.GET.get('folio_orden')
        query2 = query2[:-2] 
        query3 = self.request.GET.get('determinacion')
        return Coagulaciones.objects.filter(
            Q(nss__icontains = query) & Q(folio_orden__icontains = query2) & Q(determinacion__icontains = query3)
        )

#Editar pacientes
class PacienteEditView(UpdateView): #actualizar/editar
    model = Paciente
    fields = ('nss','nombre_paciente')
    template_name = 'editPaciente.html'
    login_url = 'login'
    success_url = reverse_lazy('pacientes')#plantilla 

def updatenotainicial(request,nss,fecha_ingreso):
    nota = Nota_inicial.objects.get(nss=nss,fecha_ingreso=fecha_ingreso)
    if nota.peso:
        nota.peso = int(nota.peso)
    if nota.talla:
        nota.talla = int(nota.talla)
    if nota.temperatura:
        nota.temperatura = int(nota.temperatura)
    if nota.frec_respiratoria:
        nota.frec_respiratoria = int(nota.frec_respiratoria)
    if nota.frec_cardiaca:
        nota.frec_cardiaca = int(nota.frec_cardiaca)
    if nota.imc:
        nota.imc = int(nota.imc)
    if nota.saturacion:
        nota.saturacion = int(nota.saturacion)
    if nota.glc_capilar:
        nota.glc_capilar = int(nota.glc_capilar)

    template = loader.get_template('edit_nota_inicial.html') 
    context = {
        'nota': nota,
    }
    return HttpResponse(template.render(context,request))    

def updaterecordnotainicial(request,nss,fecha_ingreso):
    genero = request.POST['genero']
    especialidad_ingreso = request.POST['especialidad_ingreso']
    motivo_inter = request.POST['motivo_inter']
    interrogatorio = request.POST['interrogatorio']
    dx = request.POST['dx']
    plan_tratamiento = request.POST['plan_tratamiento']
    pronostico = request.POST['pronostico']
    indicaciones = request.POST['indicaciones']
    estado_salud = request.POST['estado_salud']
    peso = request.POST['peso']
    talla = request.POST['talla']
    temperatura = request.POST['temperatura']
    frec_respiratoria = request.POST['frec_respiratoria']
    frec_cardiaca = request.POST['frec_cardiaca']
    pres_arterial = request.POST['pres_arterial']
    imc = request.POST['imc']
    saturacion = request.POST['saturacion']
    glc_capilar = request.POST['glc_capilar']
    diagnostico_inicial = request.POST['diagnostico_inicial']
    
    Nota_inicial.objects.filter(nss = nss,fecha_ingreso = fecha_ingreso).update(
        nss = nss,
        fecha_ingreso = fecha_ingreso,
        genero = genero,
        especialidad_ingreso = especialidad_ingreso,
        motivo_inter = motivo_inter,
        interrogatorio = interrogatorio,
        dx = dx,
        plan_tratamiento = plan_tratamiento,
        pronostico = pronostico,
        indicaciones = indicaciones,
        estado_salud = estado_salud,
        peso = peso,
        talla = talla,
        temperatura = temperatura,
        frec_respiratoria = frec_respiratoria,
        frec_cardiaca = frec_cardiaca,
        pres_arterial = pres_arterial,
        imc = imc,
        saturacion = saturacion,
        glc_capilar = glc_capilar,
        diagnostico_inicial = diagnostico_inicial,
    )
    return HttpResponseRedirect(reverse('pacientes'))

def updatenotaegreso(request,nss,fecha_egreso):
    nota = Nota_egreso.objects.get(nss=nss,fecha_egreso=fecha_egreso)
    fecha = str(nota.fecha_ingreso)
    fecha = fecha.replace(' de ', ' ')
    fecha = fecha.replace('enero', '01')
    fecha = fecha.replace('febrero', '02')
    fecha = fecha.replace('marzo', '03')
    fecha = fecha.replace('abril', '04')
    fecha = fecha.replace('mayo', '05')
    fecha = fecha.replace('junio', '06')
    fecha = fecha.replace('julio', '07')
    fecha = fecha.replace('agosto', '08')
    fecha = fecha.replace('septiembre', '09')
    fecha = fecha.replace('octubre', '10')
    fecha = fecha.replace('noviembre', '11')
    fecha = fecha.replace('diciembre', '12')
    fecha = fecha.replace(' ', '-')
    nota.fecha_ingreso = datetime.strptime(fecha, '%Y-%m-%d')
    nota.fecha_ingreso = nota.fecha_ingreso.strftime('%Y-%m-%d')
    if nota.peso:
        nota.peso = int(nota.peso)
    if nota.talla:
        nota.talla = int(nota.talla)
    if nota.temperatura:
        nota.temperatura = int(nota.temperatura)
    if nota.frec_respiratoria:
        nota.frec_respiratoria = int(nota.frec_respiratoria)
    if nota.frec_cardiaca:
        nota.frec_cardiaca = int(nota.frec_cardiaca)
    if nota.imc:
        nota.imc = int(nota.imc)
    if nota.saturacion:
        nota.saturacion = int(nota.saturacion)
    if nota.glc_capilar:
        nota.glc_capilar = int(nota.glc_capilar)

    template = loader.get_template('edit_nota_egreso.html') 
    context = {
        'nota': nota,
    }
    return HttpResponse(template.render(context,request)) 

       

def updaterecordnotaegreso(request,nss,fecha_egreso):
    fecha_ingreso = request.POST['fecha_ingreso']
    especialidad_egreso = request.POST['especialidad_egreso']
    motivo_egreso = request.POST['motivo_egreso']
    envio = request.POST['envio']
    diagnostico_ingreso = request.POST['diagnostico_ingreso']
    diagnostico_egreso = request.POST['diagnostico_egreso']
    resumen_evolucion = request.POST['resumen_evolucion']
    problemas_pendientes = request.POST['problemas_pendientes']
    plan_tratamiento = request.POST['plan_tratamiento']
    recomendaciones = request.POST['recomendaciones']
    factores_riesgo = request.POST['factores_riesgo']
    pronostico = request.POST['pronostico']
    diagnostico_defuncion = request.POST['diagnostico_defuncion']
    estado_salud = request.POST['estado_salud']
    peso = request.POST['peso']
    talla = request.POST['talla']
    temperatura = request.POST['temperatura']
    frec_respiratoria = request.POST['frec_respiratoria']
    frec_cardiaca = request.POST['frec_cardiaca']
    pres_arterial = request.POST['pres_arterial']
    imc = request.POST['imc']
    saturacion = request.POST['saturacion']
    glc_capilar = request.POST['glc_capilar']
    diagnostico_final = request.POST['diagnostico_final']
    
    Nota_egreso.objects.filter(nss = nss,fecha_egreso = fecha_egreso).update(
        nss = nss,
        fecha_ingreso = fecha_ingreso,
        fecha_egreso = fecha_egreso,
        especialidad_egreso = especialidad_egreso,
        motivo_egreso = motivo_egreso,
        envio = envio,
        diagnostico_ingreso = diagnostico_ingreso,
        diagnostico_egreso = diagnostico_egreso,
        resumen_evolucion = resumen_evolucion,
        problemas_pendientes = problemas_pendientes,
        plan_tratamiento = plan_tratamiento,
        recomendaciones = recomendaciones,
        factores_riesgo = factores_riesgo,
        pronostico = pronostico,
        diagnostico_defuncion = diagnostico_defuncion,
        estado_salud = estado_salud,
        peso = peso,
        talla = talla,
        temperatura = temperatura,
        frec_respiratoria = frec_respiratoria,
        frec_cardiaca = frec_cardiaca,
        pres_arterial = pres_arterial,
        imc = imc,
        saturacion = saturacion,
        glc_capilar = glc_capilar,
        diagnostico_final = diagnostico_final,
    )
    return HttpResponseRedirect(reverse('pacientes'))

def updatepruebasespeciales(request,nss,folio_orden,determinacion):
    nota = Pruebas_especiales.objects.get(nss=nss,folio_orden=folio_orden,determinacion=determinacion)
    template = loader.get_template('edit_pruebas_especiales.html') 
    context = {
        'nota': nota,
    }
    return HttpResponse(template.render(context,request))    

def updaterecordpruebasespeciales(request,nss,folio_orden,determinacion):
    resultado = request.POST['resultado']
    unidad = request.POST['unidad']
    valor_normal = request.POST['valor_normal']
    
    Pruebas_especiales.objects.filter(nss = nss,folio_orden = folio_orden, determinacion = determinacion).update(
        nss = nss,
        folio_orden = folio_orden,
        determinacion = determinacion,
        resultado = resultado,
        unidad = unidad,
        valor_normal = valor_normal,
    )
    return HttpResponseRedirect(reverse('pacientes'))

def updatequimicaclinica(request,nss,folio_orden,determinacion):
    nota = Quimica_clinica.objects.get(nss=nss,folio_orden=folio_orden,determinacion=determinacion)
    template = loader.get_template('edit_quimica_clinica.html') 
    context = {
        'nota': nota,
    }
    return HttpResponse(template.render(context,request))    

def updaterecordquimicaclinica(request,nss,folio_orden,determinacion):
    resultado = request.POST['resultado']
    unidad = request.POST['unidad']
    valor_normal = request.POST['valor_normal']
    
    Quimica_clinica.objects.filter(nss = nss,folio_orden = folio_orden, determinacion = determinacion).update(
        nss = nss,
        folio_orden = folio_orden,
        determinacion = determinacion,
        resultado = resultado,
        unidad = unidad,
        valor_normal = valor_normal,
    )
    return HttpResponseRedirect(reverse('pacientes'))

def updatemedicinanuclear(request,nss,folio_orden,determinacion):
    nota = Medicina_nuclear.objects.get(nss=nss,folio_orden=folio_orden,determinacion=determinacion)
    template = loader.get_template('edit_medicina_nuclear.html') 
    context = {
        'nota': nota,
    }
    return HttpResponse(template.render(context,request)) 

def updaterecordmedicinanuclear(request,nss,folio_orden,determinacion):
    resultado = request.POST['resultado']
    unidad = request.POST['unidad']
    valor_normal = request.POST['valor_normal']
    
    Medicina_nuclear.objects.filter(nss = nss,folio_orden = folio_orden, determinacion = determinacion).update(
        nss = nss,
        folio_orden = folio_orden,
        determinacion = determinacion,
        resultado = resultado,
        unidad = unidad,
        valor_normal = valor_normal,
    )
    return HttpResponseRedirect(reverse('pacientes'))

def updatelaboratorio(request,nss,folio_orden):
    nota = Laboratorio.objects.get(nss=nss,folio_orden=folio_orden)
    fecha = str(nota.fecha_orden)
    fecha = fecha.replace(' de ', ' ')
    fecha = fecha.replace('enero', '01')
    fecha = fecha.replace('febrero', '02')
    fecha = fecha.replace('marzo', '03')
    fecha = fecha.replace('abril', '04')
    fecha = fecha.replace('mayo', '05')
    fecha = fecha.replace('junio', '06')
    fecha = fecha.replace('julio', '07')
    fecha = fecha.replace('agosto', '08')
    fecha = fecha.replace('septiembre', '09')
    fecha = fecha.replace('octubre', '10')
    fecha = fecha.replace('noviembre', '11')
    fecha = fecha.replace('diciembre', '12')
    fecha = fecha.replace(' ', '-')
    nota.fecha_orden = datetime.strptime(fecha, '%Y-%m-%d')
    nota.fecha_orden = nota.fecha_orden.strftime('%Y-%m-%d')
    template = loader.get_template('edit_laboratorio.html') 
    context = {
        'nota': nota,
    }
    return HttpResponse(template.render(context,request)) 

def updaterecordlaboratorio(request,nss,folio_orden):
    fecha_orden = request.POST['fecha_orden']
    edad = request.POST['edad']
    servicio_solicita = request.POST['servicio_solicita']
    
    Laboratorio.objects.filter(nss = nss,folio_orden = folio_orden).update(
        nss = nss,
        folio_orden = folio_orden,
        fecha_orden = fecha_orden,
        edad = edad,
        servicio_solicita = servicio_solicita,
    )
    return HttpResponseRedirect(reverse('pacientes'))

def updateinmunologia(request,nss,folio_orden,determinacion):
    nota = Inmunologia.objects.get(nss=nss,folio_orden=folio_orden,determinacion=determinacion)
    template = loader.get_template('edit_inmunologia.html') 
    context = {
        'nota': nota,
    }
    return HttpResponse(template.render(context,request)) 

def updaterecordinmunologia(request,nss,folio_orden,determinacion):
    resultado = request.POST['resultado']
    unidad = request.POST['unidad']
    valor_normal = request.POST['valor_normal']
    
    Inmunologia.objects.filter(nss = nss,folio_orden = folio_orden, determinacion = determinacion).update(
        nss = nss,
        folio_orden = folio_orden,
        determinacion = determinacion,
        resultado = resultado,
        unidad = unidad,
        valor_normal = valor_normal,
    )
    return HttpResponseRedirect(reverse('pacientes'))

def updateinmunoinfecto(request,nss,folio_orden,determinacion):
    nota = Inmuno_infecto.objects.get(nss=nss,folio_orden=folio_orden,determinacion=determinacion)
    template = loader.get_template('edit_inmuno_infecto.html') 
    context = {
        'nota': nota,
    }
    return HttpResponse(template.render(context,request)) 

def updaterecordinmunoinfecto(request,nss,folio_orden,determinacion):
    resultado = request.POST['resultado']
    unidad = request.POST['unidad']
    valor_normal = request.POST['valor_normal']
    
    Inmuno_infecto.objects.filter(nss = nss,folio_orden = folio_orden, determinacion = determinacion).update(
        nss = nss,
        folio_orden = folio_orden,
        determinacion = determinacion,
        resultado = resultado,
        unidad = unidad,
        valor_normal = valor_normal,
    )
    return HttpResponseRedirect(reverse('pacientes'))

def updatehematologia(request,nss,folio_orden,determinacion):
    nota = Hematologia.objects.get(nss=nss,folio_orden=folio_orden,determinacion=determinacion)
    template = loader.get_template('edit_hematologia.html') 
    context = {
        'nota': nota,
    }
    return HttpResponse(template.render(context,request)) 

def updaterecordhematologia(request,nss,folio_orden,determinacion):
    resultado = request.POST['resultado']
    unidad = request.POST['unidad']
    valor_normal = request.POST['valor_normal']
    
    Hematologia.objects.filter(nss = nss,folio_orden = folio_orden, determinacion = determinacion).update(
        nss = nss,
        folio_orden = folio_orden,
        determinacion = determinacion,
        resultado = resultado,
        unidad = unidad,
        valor_normal = valor_normal,
    )
    return HttpResponseRedirect(reverse('pacientes'))

def updatedrogasterapeuticas(request,nss,folio_orden,determinacion):
    nota = Drogas_terapeuticas.objects.get(nss=nss,folio_orden=folio_orden,determinacion=determinacion)
    template = loader.get_template('edit_drogas_terapeuticas.html') 
    context = {
        'nota': nota,
    }
    return HttpResponse(template.render(context,request)) 

def updaterecorddrogasterapeuticas(request,nss,folio_orden,determinacion):
    resultado = request.POST['resultado']
    unidad = request.POST['unidad']
    valor_normal = request.POST['valor_normal']
    
    Drogas_terapeuticas.objects.filter(nss = nss,folio_orden = folio_orden, determinacion = determinacion).update(
        nss = nss,
        folio_orden = folio_orden,
        determinacion = determinacion,
        resultado = resultado,
        unidad = unidad,
        valor_normal = valor_normal,
    )
    return HttpResponseRedirect(reverse('pacientes'))

def updatecoagulaciones(request,nss,folio_orden,determinacion):
    nota = Coagulaciones.objects.get(nss=nss,folio_orden=folio_orden,determinacion=determinacion)
    template = loader.get_template('edit_coagulaciones.html') 
    context = {
        'nota': nota,
    }
    return HttpResponse(template.render(context,request)) 

def updaterecordcoagulaciones(request,nss,folio_orden,determinacion):
    resultado = request.POST['resultado']
    unidad = request.POST['unidad']
    valor_normal = request.POST['valor_normal']
    
    Coagulaciones.objects.filter(nss = nss,folio_orden = folio_orden, determinacion = determinacion).update(
        nss = nss,
        folio_orden = folio_orden,
        determinacion = determinacion,
        resultado = resultado,
        unidad = unidad,
        valor_normal = valor_normal,
    )
    return HttpResponseRedirect(reverse('pacientes'))

class PacienteDeleteView(DeleteView): #borrar
    model = Paciente
    template_name = 'paciente_delete.html'
    login_url = 'login'  
    success_url = reverse_lazy('pacientes')#plantilla 

    """ def dispatch(self, form): #permiso para autentificados
        if self.request.user.is_superuser:
            return super().dispatch(form)
        return redirect('error')  """

def deletenotainicial(request,nss,fecha_ingreso):
    if request.user.is_superuser:
        Nota_inicial.objects.filter(nss = nss,fecha_ingreso = fecha_ingreso).delete()
        return HttpResponseRedirect(reverse('pacientes'))
    return redirect('error') 

def deletenotaegreso(request,nss,fecha_egreso):
    if request.user.is_superuser:
        Nota_egreso.objects.filter(nss = nss,fecha_egreso = fecha_egreso).delete()
        return HttpResponseRedirect(reverse('pacientes'))
    return redirect('error') 

def deletepruebasespeciales(request,nss,folio_orden,determinacion):
    if request.user.is_superuser:
        Pruebas_especiales.objects.filter(nss = nss,folio_orden = folio_orden, determinacion = determinacion).delete()
        return HttpResponseRedirect(reverse('pacientes'))
    return redirect('error') 

def deletequimicaclinica(request,nss,folio_orden,determinacion):
    if request.user.is_superuser:
        Quimica_clinica.objects.filter(nss = nss,folio_orden = folio_orden, determinacion = determinacion).delete()
        return HttpResponseRedirect(reverse('pacientes'))
    return redirect('error') 

def deletemedicinanuclear(request,nss,folio_orden,determinacion):
    if request.user.is_superuser:
        Medicina_nuclear.objects.filter(nss = nss,folio_orden = folio_orden, determinacion = determinacion).delete()
        return HttpResponseRedirect(reverse('pacientes'))
    return redirect('error') 

def deletelaboratorio(request,nss,folio_orden):
    if request.user.is_superuser:
        Laboratorio.objects.filter(nss = nss,folio_orden = folio_orden).delete()
        return HttpResponseRedirect(reverse('pacientes'))
    return redirect('error') 

def deleteinmunologia(request,nss,folio_orden,determinacion):
    if request.user.is_superuser:
        Inmunologia.objects.filter(nss = nss,folio_orden = folio_orden, determinacion = determinacion).delete()
        return HttpResponseRedirect(reverse('pacientes'))
    return redirect('error') 

def deleteinmunoinfecto(request,nss,folio_orden,determinacion):
    if request.user.is_superuser:
        Inmuno_infecto.objects.filter(nss = nss,folio_orden = folio_orden, determinacion = determinacion).delete()
        return HttpResponseRedirect(reverse('pacientes'))
    return redirect('error') 

def deletehematologia(request,nss,folio_orden,determinacion):
    if request.user.is_superuser:
        Hematologia.objects.filter(nss = nss,folio_orden = folio_orden, determinacion = determinacion).delete()
        return HttpResponseRedirect(reverse('pacientes'))
    return redirect('error') 

def deletedrogasterapeuticas(request,nss,folio_orden,determinacion):
    if request.user.is_superuser:
        Drogas_terapeuticas.objects.filter(nss = nss,folio_orden = folio_orden, determinacion = determinacion).delete()
        return HttpResponseRedirect(reverse('pacientes'))
    return redirect('error') 

def deletecoagulaciones(request,nss,folio_orden,determinacion):
    if request.user.is_superuser:
        Coagulaciones.objects.filter(nss = nss,folio_orden = folio_orden, determinacion = determinacion).delete()
        return HttpResponseRedirect(reverse('pacientes'))
    return redirect('error') 


from django.views.generic.edit import FormView
from .forms import FileFieldForm

#pdf 
import Funciones.PDFSupports as pdfSupports
import Funciones.PDFWorks as pdfWorks
import Funciones.SQLconnect as sqlconnect

class upload(FormView):
    form_class = FileFieldForm
    template_name = 'upload.html'  # Replace with your template.
    success_url = reverse_lazy('pacientes')#plantilla

    def post(self, request, *args, **kwargs):

        context = {}
        context['Notas_Ingreso'] = []
        context['Notas_Ingreso_fallo'] = []
        context['Notas_Interconsulta'] = []
        context['Notas_Interconsulta_fallo'] = []
        context['Notas_Egreso'] = []
        context['Notas_Egreso_fallo'] = []
        context['Laboratorios'] = []
        context['Laboratorios_fallo'] = []
        context['Otros'] = []
        context['Otros_fallo'] = []

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        rutasCarpetas = pdfSupports.rutasCarpetas()
        if form.is_valid():
            for f in files:
                fs = FileSystemStorage()
                fs.save(f.name, f)

            rutasCarpetas = pdfSupports.rutasCarpetas()

            pdfsParaEvaluar=pdfWorks.pdfsPendientes(rutasCarpetas[1][6])
            #1.3-Organizar cada PDF pendiente (si hay)
            if pdfsParaEvaluar[0]>0:
                for evalRutaPDF in pdfsParaEvaluar[1]:
                    pdfWorks.pdfsOrganizar(rutasCarpetas[0][0],rutasCarpetas[1],rutasCarpetas[2],evalRutaPDF)
            else:
                print("No hay archivos pdfs pendientes a organizar\n")

            nombreTabla='paciente_nota_inicial'

            #CONEXION CON MYSQL
            archivos_en_bd=sqlconnect.DBStatusTables(nombreTabla)

            #Creacion de diccionario para Pickle
            dicPacientes_NotaInicial=pdfWorks.pdfsNotaInicial(rutasCarpetas[0][0],rutasCarpetas[1][1],rutasCarpetas[1][5],archivos_en_bd)

            #Guardar diccionario en pickle para consulta rapida
            pdfSupports.pickleGuardarDic(dicPacientes_NotaInicial[0],'Pacientes')
            pdfSupports.pickleGuardarDic(dicPacientes_NotaInicial[1],'NotaInicial')

            nombreTabla = 'paciente_laboratorio'

            # CONEXION CON MYSQL
            archivos_en_bd=sqlconnect.DBStatusTables(nombreTabla)

            #Creacion de diccionario para Pickle
            dicPacientes_Laboratorio = pdfWorks.pdfsLaboratorio(rutasCarpetas[0][0], rutasCarpetas[1][4],rutasCarpetas[1][5],archivos_en_bd)

            #Guardar diccionario en pickle para consulta rapida
            pdfSupports.pickleGuardarDic(dicPacientes_Laboratorio,'Laboratorio')

            nombreTabla = 'paciente_nota_egreso'

            # CONEXION CON MYSQL
            archivos_en_bd=sqlconnect.DBStatusTables(nombreTabla)

            #Creacion de diccionario para Pickle
            dicPacientes_NotaEgreso = pdfWorks.pdfsNotaEgreso(rutasCarpetas[0][0], rutasCarpetas[1][3],rutasCarpetas[1][5],archivos_en_bd)

            #Guardar diccionario en pickle para consulta rapida
            pdfSupports.pickleGuardarDic(dicPacientes_NotaEgreso,'NotaEgreso')

            #3.1-Cargar diccionarios de Pickle
            pickleDiccionarios = pdfSupports.pickleCargarDic(rutasCarpetas[0][0])

            if (pickleDiccionarios):
                #3.2-Consultar a BASE DE DATOS
                sqlconnect.DBmanager(pickleDiccionarios)                   #Agregar opcion de llenado a base de datos

            #3.1-Cargar diccionarios de Pickle
            pickleDiccionarios = pdfSupports.pickleCargarDic(rutasCarpetas[0][0])

            if (pickleDiccionarios):
                #3.2-Consultar a BASE DE DATOS
                sqlconnect.DBmanager(pickleDiccionarios)                   #Agregar opcion de llenado a base de datos

            #3.1-Cargar diccionarios de Pickle
            pickleDiccionarios = pdfSupports.pickleCargarDic(rutasCarpetas[0][0])

            if (pickleDiccionarios):
                #3.2-Consultar a BASE DE DATOS
                sqlconnect.DBmanager(pickleDiccionarios)                   #Agregar opcion de llenado a base de datos

                #ejemplo_dir = '/Users/kenia/Desktop/Diag8/Modular2-Alexa/DatosClinicos/1-Notas_Ingreso'  #C:\Users\kenia\Desktop\Diag8\Modular2-Alexa\DatosClinicos\1-Notas_Ingreso
                rutaActual = os.path.abspath(os.getcwd())
                ejemplo_dir = rutaActual + '\\DatosClinicos\\1-Notas_Ingreso'
                with os.scandir(ejemplo_dir) as ficheros:
                    dir = os.listdir(ejemplo_dir)
                    if len(dir) == 0:
                        pass
                    else:
                        for fichero in ficheros:
                            nss = fichero.name[0:10]
                            nss = float(nss)
                            nss = floor(nss)

                            try:
                                Notas = Paciente.objects.get(nss=nss)
                            except Paciente.DoesNotExist:
                                context['Notas_Ingreso_fallo'].append(nss)

                            if Notas:
                                context['Notas_Ingreso'].append(nss)

                            ####sacar el nombreeeeeeeeeeeeeeeeeeeeeeeeeeeeee
                            pdfFileObj = open(fichero, 'rb')
                            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                            pageObj = pdfReader.getPage(0)
                            text=(pageObj.extractText())
                            text=text.split(",")

                            search_keywords = ['Nombre Paciente']
                            sentence = ''
                            for sentence in text:
                                lst = []
                                for word in search_keywords:
                                    if word in sentence:
                                        buena = sentence.split('\n')
                                        break

                            for i in range(len(buena)):
                                if 'Nombre' in buena[i]:
                                    indice = i

                            Nombre =  buena[indice]
                            Nombre =  Nombre.replace('Nombre Paciente:', '')
                            Nombre = Nombre.lower()

                            Paciente.objects.filter(nss=nss).update(nss=nss,nombre_paciente=Nombre)
                            pdfFileObj.close()
                            remove(fichero)
                #2 Borrar nota interconsulta
                #ejemplo_dir2 = '/Users/kenia/Desktop/Diag8/Modular2-Alexa/DatosClinicos/2-Notas_Interconsulta'  #C:\Users\kenia\Desktop\Diag8\Modular2-Alexa\DatosClinicos\1-Notas_Ingreso
                rutaActual = os.path.abspath(os.getcwd())
                ejemplo_dir2 = rutaActual + '\\DatosClinicos\\2-Notas_Interconsulta'
                with os.scandir(ejemplo_dir2) as ficheros2:
                    dir2 = os.listdir(ejemplo_dir2)
                    if len(dir2) == 0:
                        pass
                    else:
                        for fichero2 in ficheros2:
                            nss = fichero2.name[0:10]
                            nss = float(nss)
                            nss = floor(nss)
                            try:
                                Notas = Paciente.objects.get(nss=nss)
                            except:
                                context['Notas_Interconsulta_fallo'].append(nss)

                            if Notas:
                                context['Notas_Interconsulta'].append(nss)

                            remove(fichero2)
                #3 Borrar notas egreso de neumonia
                #ejemplo_dir3 = '/Users/kenia/Desktop/Diag8/Modular2-Alexa/DatosClinicos/3-Notas_Egreso/1-Neumonia'  #C:\Users\kenia\Desktop\Diag6\diagnostico\DatosClinicos\1-Notas_Ingreso
                rutaActual = os.path.abspath(os.getcwd())
                ejemplo_dir3 = rutaActual + '\\DatosClinicos\\3-Notas_Egreso\\1-Neumonia'
                with os.scandir(ejemplo_dir3) as ficheros3:
                    dir3 = os.listdir(ejemplo_dir3)
                    if len(dir3) == 0:
                        pass
                    else:
                        for fichero3 in ficheros3:
                            print("Soy los nombres del fichero 3 de Neumonia",fichero3.name)
                            nss = fichero3.name[0:10]
                            nss = float(nss)
                            nss = floor(nss)
            
                            try:
                                Notas = Paciente.objects.get(nss=nss)
                                context['Notas_Egreso'].append(nss)
                            except:
                                context['Notas_Egreso_fallo'].append(nss)

                            remove(fichero3)
                #borrar notas egreso de embolia
                #ejemplo_dir31 = '/Users/kenia/Desktop/Diag8/Modular2-Alexa/DatosClinicos/3-Notas_Egreso/2-Embolia'  #C:\Users\kenia\Desktop\Diag6\diagnostico\DatosClinicos\1-Notas_Ingreso
                rutaActual = os.path.abspath(os.getcwd())
                ejemplo_dir31 = rutaActual + '\\DatosClinicos\\3-Notas_Egreso\\2-Embolia'
                with os.scandir(ejemplo_dir31) as ficheros31:
                    dir31 = os.listdir(ejemplo_dir31)
                    if len(dir31) == 0:
                        pass
                    else:
                        for fichero31 in ficheros31:
                            nss = fichero31.name[0:10]
                            nss = float(nss)
                            nss = floor(nss)
    
                            try:
                                Notas = Paciente.objects.get(nss=nss)
                                context['Notas_Egreso'].append(nss)
                            except:
                                context['Notas_Egreso_fallo'].append(nss)

                            remove(fichero31)
                #borrar notas egreso de control
                #ejemplo_dir32 = '/Users/kenia/Desktop/Diag8/Modular2-Alexa/DatosClinicos/3-Notas_Egreso/3-Control'  #C:\Users\kenia\Desktop\Diag6\diagnostico\DatosClinicos\1-Notas_Ingreso
                rutaActual = os.path.abspath(os.getcwd())
                ejemplo_dir32 = rutaActual + '\\DatosClinicos\\3-Notas_Egreso\\3-Control'
                with os.scandir(ejemplo_dir32) as ficheros32:
                    dir32 = os.listdir(ejemplo_dir32)
                    if len(dir32) == 0:
                        pass
                    else:
                        for fichero32 in ficheros32:
                            nss = fichero32.name[0:10]
                            nss = float(nss)
                            nss = floor(nss)
                            try:
                                Notas = Paciente.objects.get(nss=nss)
                            except:
                                context['Notas_Egreso_fallo'].append(nss)

                            if Notas:
                                context['Notas_Egreso'].append(nss)

                            remove(fichero32)
                #borrar notas egreso de Otros
                #ejemplo_dir33 = '/Users/kenia/Desktop/Diag8/Modular2-Alexa/DatosClinicos/3-Notas_Egreso/4-Otros'  #C:\Users\kenia\Desktop\Diag6\diagnostico\DatosClinicos\1-Notas_Ingreso
                rutaActual = os.path.abspath(os.getcwd())
                ejemplo_dir33 = rutaActual + '\\DatosClinicos\\3-Notas_Egreso\\4-Otros'
                with os.scandir(ejemplo_dir33) as ficheros33:
                    dir33 = os.listdir(ejemplo_dir33)
                    if len(dir33) == 0:
                        pass
                    else:
                        for fichero33 in ficheros33:
                            nss = fichero33.name[0:10]
                            nss = float(nss)
                            nss = floor(nss)
                            try:
                                Notas = Paciente.objects.get(nss=nss)
                            except:
                                context['Notas_Egreso_fallo'].append(nss)

                            if Notas:
                                context['Notas_Egreso'].append(nss)

                            remove(fichero33)
                #4 Laboratorios
                #ejemplo_dir4 = '/Users/kenia/Desktop/Diag8/Modular2-Alexa/DatosClinicos/4-Laboratorios'  #C:\Users\kenia\Desktop\Diag8\Modular2-Alexa\DatosClinicos\4-Laboratorios
                rutaActual = os.path.abspath(os.getcwd())
                ejemplo_dir4 = rutaActual + '\\DatosClinicos\\4-Laboratorios'
                with os.scandir(ejemplo_dir4) as ficheros4:
                    dir4 = os.listdir(ejemplo_dir4)
                    if len(dir4) == 0:
                        pass
                    else:
                        for fichero4 in ficheros4:
                            nss = fichero4.name[0:10]
                            nss = float(nss)
                            nss = floor(nss)
                            try:
                                Notas = Paciente.objects.get(nss=nss)
                            except:
                                context['Laboratorios_fallo'].append(nss)

                            if Notas:
                                context['Laboratorios'].append(nss)
                                
                            remove(fichero4)
                #5 Otros
                #ejemplo_dir5 = '/Users/kenia/Desktop/Diag8/Modular2-Alexa/DatosClinicos/5-Otros'  #C:\Users\kenia\Desktop\Diag6\diagnostico\DatosClinicos\1-Notas_Ingreso
                rutaActual = os.path.abspath(os.getcwd())
                ejemplo_dir5 = rutaActual + '\\DatosClinicos\\5-Otros'
                with os.scandir(ejemplo_dir5) as ficheros5:
                    dir5 = os.listdir(ejemplo_dir5)
                    if len(dir5) == 0:
                        pass
                    else:
                        for fichero5 in ficheros5:
                            nss = fichero5.name[10:20]##########################
                            print(nss)
                            nss = float(nss)
                            nss = floor(nss)
                            try:
                                Notas = Paciente.objects.get(nss=nss)
                            except:
                                context['Otros_fallo'].append(nss)

                            if Notas:
                                context['Otros'].append(nss)

                            remove(fichero5)

            template = loader.get_template('detalles.html') 
            backup.backup()
            return HttpResponse(template.render(context,request)) 

        else:
            return self.form_invalid(form)

    def dispatch(self, form): #permiso para autentificados
        if self.request.user.is_authenticated:
            return super().dispatch(form)
        return redirect('error') 

class DetallesView(TemplateView):
    template_name = "detalles.html"