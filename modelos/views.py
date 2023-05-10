from django.shortcuts import render
from django.views.generic import TemplateView
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import Funciones.modelos as md

import json
import pandas as pd
import os
from threading import Thread

class ThreadWithReturnValue(Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            print(f'running Thread {self.name}')
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'modelos.html'

class informationView(TemplateView):
    template_name = 'informacionmodelos.html'    

#Formulario filtros
def form_filtros(request):
    template = loader.get_template('filtros.html')
    context = {}
    return HttpResponse(template.render(context,request))

def filtros(request):
    genero = request.POST['genero']
    edad_min = request.POST['edad_min']
    edad_max = request.POST['edad_max']
    fecha_ingreso_ini = request.POST['fecha_ingreso_ini']
    fecha_ingreso_fin = request.POST['fecha_ingreso_fin']

    algoritmo = request.POST['modelos']

    KNN_3_Form = request.POST.get('KNN_3_Form', False)
    KNN_NE_Form = request.POST.get('KNN_NE_Form', False)
    KNN_NC_Form = request.POST.get('KNN_NC_Form', False)
    KNN_EC_Form = request.POST.get('KNN_EC_Form', False)
    KNN_NO_Form = request.POST.get('KNN_NO_Form', False)
    KNN_EO_Form = request.POST.get('KNN_EO_Form', False)

    X, NSS_pacientes = md.datos_lab_filtros(genero, edad_min, edad_max, fecha_ingreso_ini, fecha_ingreso_fin)

    data = []
    
    NSS_pacientes['nss'] = NSS_pacientes['nss'].astype(str) #mapping numbers
    NSS_pacientes['nss'] = NSS_pacientes['nss'].str[:-2]
    NSS_pacientes['genero'] = NSS_pacientes['genero'].map({'f' : 'femenino', 'm' : 'masculino'}).astype(str) #mapping numbers
    reporte = NSS_pacientes
    lista_hilos=[]
    
    context = {}
    context['modelo'] = algoritmo
    
    if(algoritmo == 'KNN'):
        context['NEC'] = 'Exactitud: 57%'
        context['NE'] = 'Exactitud: 70%'
        context['NC'] = 'Exactitud: 71%'
        context['EC'] = 'Exactitud: 65%'
        context['NO'] = 'Exactitud: 65%'
        context['EO'] = 'Exactitud: 68%'
    elif(algoritmo == 'DT'):
        context['NEC'] = 'Exactitud: 65%'
        context['NE'] = 'Exactitud: 73%'
        context['NC'] = 'Exactitud: 73%'
        context['EC'] = 'Exactitud: 65%'
        context['NO'] = 'Exactitud: 68%'
        context['EO'] = 'Exactitud: 60%'
    elif(algoritmo == 'MLP'):
        context['NEC'] = 'Exactitud: 60%'
        context['NE'] = 'Exactitud: 75%'
        context['NC'] = 'Exactitud: 73%'
        context['EC'] = 'Exactitud: 67%'
        context['NO'] = 'Exactitud: 68%'
        context['EO'] = 'Exactitud: 77%'
    elif(algoritmo == 'NB'):
        context['NEC'] = 'Exactitud: 78%'
        context['NE'] = 'Exactitud: 80%'
        context['NC'] = 'Exactitud: 75%'
        context['EC'] = 'Exactitud: 57%'
        context['NO'] = 'Exactitud: 45%'
        context['EO'] = 'Exactitud: 55%'
    elif(algoritmo == 'SVM'):
        context['NEC'] = 'Exactitud: 80%'
        context['NE'] = 'Exactitud: 83%'
        context['NC'] = 'Exactitud: 59%'
        context['EC'] = 'Exactitud: 50%'
        context['NO'] = 'Exactitud: 69%'
        context['EO'] = 'Exactitud: 65%'

    if algoritmo == 'KNN':

        # 3 Diagnosticos: Neumonia - Embolia - Control
        if KNN_3_Form == 'on':
            
            hilo1 = ThreadWithReturnValue(target=md.KNN_3diag,args=(X, NSS_pacientes,reporte),name='hilo1')
            lista_hilos.append(hilo1)

        # 2 Diagnosticos
        # Neumonia - Embolia
        if KNN_NE_Form == 'on':

            hilo2 = ThreadWithReturnValue(target=md.KNN_N_E,args=(X, NSS_pacientes,reporte),name='hilo2')
            lista_hilos.append(hilo2)

        # Neumonia - Control
        if KNN_NC_Form == 'on':

            hilo3 = ThreadWithReturnValue(target=md.KNN_N_C,args=(X, NSS_pacientes,reporte),name='hilo3')
            lista_hilos.append(hilo3)

        # Embolia - Control
        if KNN_EC_Form == 'on':

            hilo4 = ThreadWithReturnValue(target=md.KNN_E_C,args=(X, NSS_pacientes,reporte),name='hilo4')
            lista_hilos.append(hilo4)

        # Neumonia - NoNeumonia
        if KNN_NO_Form == 'on':

            hilo5 = ThreadWithReturnValue(target=md.KNN_N_O,args=(X, NSS_pacientes,reporte),name='hilo5')
            lista_hilos.append(hilo5)

        # Embolia - NoEmbolia
        if KNN_EO_Form == 'on':

            hilo6 = ThreadWithReturnValue(target=md.KNN_E_O,args=(X, NSS_pacientes,reporte),name='hilo6')
            lista_hilos.append(hilo6)
            
        for i in lista_hilos:
            i.start()
        
        for i in lista_hilos:
            reporte2 = i.join()
            reporte = pd.merge(reporte,reporte2)

    elif algoritmo == 'DT':

        # 3 Diagnosticos: Neumonia - Embolia - Control
        if KNN_3_Form == 'on':

            hilo1 = ThreadWithReturnValue(target=md.DT_3diag,args=(X, NSS_pacientes,reporte),name='hilo1')
            lista_hilos.append(hilo1)

        # 2 Diagnosticos
        # Neumonia - Embolia
        if KNN_NE_Form == 'on':

            hilo2 = ThreadWithReturnValue(target=md.DT_N_E,args=(X, NSS_pacientes,reporte),name='hilo2')
            lista_hilos.append(hilo2)

        # Neumonia - Control
        if KNN_NC_Form == 'on':

            hilo3 = ThreadWithReturnValue(target=md.DT_N_C,args=(X, NSS_pacientes,reporte),name='hilo3')
            lista_hilos.append(hilo3)

        # Embolia - Control
        if KNN_EC_Form == 'on':

            hilo4 = ThreadWithReturnValue(target=md.DT_E_C,args=(X, NSS_pacientes,reporte),name='hilo4')
            lista_hilos.append(hilo4)

        # Neumonia - NoNeumonia
        if KNN_NO_Form == 'on':

            hilo5 = ThreadWithReturnValue(target=md.DT_N_O,args=(X, NSS_pacientes,reporte),name='hilo5')
            lista_hilos.append(hilo5)

        # Embolia - NoEmbolia
        if KNN_EO_Form == 'on':

            hilo6 = ThreadWithReturnValue(target=md.DT_E_O,args=(X, NSS_pacientes,reporte),name='hilo6')
            lista_hilos.append(hilo6)
            
        for i in lista_hilos:
            i.start()
            
        for i in lista_hilos:
            reporte2 = i.join()
            reporte = pd.merge(reporte,reporte2)

    elif algoritmo == 'MLP':

        # 3 Diagnosticos: Neumonia - Embolia - Control
        if KNN_3_Form == 'on':

            hilo1 = ThreadWithReturnValue(target=md.MLP_3diag,args=(X, NSS_pacientes,reporte),name='hilo1')
            lista_hilos.append(hilo1)

        # 2 Diagnosticos
        # Neumonia - Embolia
        if KNN_NE_Form == 'on':

            hilo2 = ThreadWithReturnValue(target=md.MLP_N_E,args=(X, NSS_pacientes,reporte),name='hilo2')
            lista_hilos.append(hilo2)

        # Neumonia - Control
        if KNN_NC_Form == 'on':

           hilo3 = ThreadWithReturnValue(target=md.MLP_N_C,args=(X, NSS_pacientes,reporte),name='hilo3')
           lista_hilos.append(hilo3)

        # Embolia - Control
        if KNN_EC_Form == 'on':

            hilo4 = ThreadWithReturnValue(target=md.MLP_E_C,args=(X, NSS_pacientes,reporte),name='hilo4')
            lista_hilos.append(hilo4)

        # Neumonia - NoNeumonia
        if KNN_NO_Form == 'on':

            hilo5 = ThreadWithReturnValue(target=md.MLP_N_O,args=(X, NSS_pacientes,reporte),name='hilo5')
            lista_hilos.append(hilo5)

        # Embolia - NoEmbolia
        if KNN_EO_Form == 'on':

            hilo6 = ThreadWithReturnValue(target=md.MLP_E_O,args=(X, NSS_pacientes,reporte),name='hilo6')
            lista_hilos.append(hilo6)
            
        for i in lista_hilos:
            i.start()
            
        for i in lista_hilos:
            reporte2 = i.join()
            reporte = pd.merge(reporte,reporte2)

    elif algoritmo == 'NB':

        # 3 Diagnosticos: Neumonia - Embolia - Control
        if KNN_3_Form == 'on':

            hilo1 = ThreadWithReturnValue(target=md.NB_3diag,args=(X, NSS_pacientes,reporte),name='hilo1')
            lista_hilos.append(hilo1)

        # 2 Diagnosticos
        # Neumonia - Embolia
        if KNN_NE_Form == 'on':

            hilo2 = ThreadWithReturnValue(target=md.NB_N_E,args=(X, NSS_pacientes,reporte),name='hilo2')
            lista_hilos.append(hilo2)

        # Neumonia - Control
        if KNN_NC_Form == 'on':

            hilo3 = ThreadWithReturnValue(target=md.NB_N_C,args=(X, NSS_pacientes,reporte),name='hilo3')
            lista_hilos.append(hilo3)

        # Embolia - Control
        if KNN_EC_Form == 'on':

            hilo4 = ThreadWithReturnValue(target=md.NB_E_C,args=(X, NSS_pacientes,reporte),name='hilo4')
            lista_hilos.append(hilo4)

        # Neumonia - NoNeumonia
        if KNN_NO_Form == 'on':

            hilo5 = ThreadWithReturnValue(target=md.NB_N_O,args=(X, NSS_pacientes,reporte),name='hilo5')
            lista_hilos.append(hilo5)

        # Embolia - NoEmbolia
        if KNN_EO_Form == 'on':

            hilo6 = ThreadWithReturnValue(target=md.NB_E_O,args=(X, NSS_pacientes,reporte),name='hilo6')
            lista_hilos.append(hilo6)
            
        for i in lista_hilos:
            i.start()
            
        for i in lista_hilos:
            reporte2 = i.join()
            reporte = pd.merge(reporte,reporte2)

    elif algoritmo == 'SVM':

        # 3 Diagnosticos: Neumonia - Embolia - Control
        if KNN_3_Form == 'on':

            hilo1 = ThreadWithReturnValue(target=md.SVM_3diag,args=(X, NSS_pacientes,reporte),name='hilo1')
            lista_hilos.append(hilo1)

        # 2 Diagnosticos
        # Neumonia - Embolia
        if KNN_NE_Form == 'on':

            hilo2 = ThreadWithReturnValue(target=md.SVM_N_E,args=(X, NSS_pacientes,reporte),name='hilo2')
            lista_hilos.append(hilo2)

        # Neumonia - Control
        if KNN_NC_Form == 'on':

            hilo3 = ThreadWithReturnValue(target=md.SVM_N_C,args=(X, NSS_pacientes,reporte),name='hilo3')
            lista_hilos.append(hilo3)

        # Embolia - Control
        if KNN_EC_Form == 'on':

            hilo4 = ThreadWithReturnValue(target=md.SVM_E_C,args=(X, NSS_pacientes,reporte),name='hilo4')
            lista_hilos.append(hilo4)

        # Neumonia - NoNeumonia
        if KNN_NO_Form == 'on':

            hilo5 = ThreadWithReturnValue(target=md.SVM_N_O,args=(X, NSS_pacientes,reporte),name='hilo5')
            lista_hilos.append(hilo5)

        # Embolia - NoEmbolia
        if KNN_EO_Form == 'on':

            hilo6 = ThreadWithReturnValue(target=md.SVM_E_O,args=(X, NSS_pacientes,reporte),name='hilo6')
            lista_hilos.append(hilo6)
            
        for i in lista_hilos:
            i.start()
        
        for i in lista_hilos:
            reporte2 = i.join()
            reporte = pd.merge(reporte,reporte2)
            
    col = []
    for column in reporte.columns:
        col.append(column)

    reporte = reporte.set_index('nss')
    # parsing the DataFrame in json format.
    json_records = reporte.reset_index().to_json(orient = 'records')
    data.append(json.loads(json_records))
    rutaActual = os.path.abspath(os.getcwd())
    name = 'Reporte'
    reporte.to_csv(str(rutaActual) + '\\'+str(name)+'.csv', index=True, header=True)

    for j in data:
        for i in j:
            fechita = i['fecha_ingreso']
            i['fecha_ingreso'] = fechita[0:11]
    
    context['d'] = data
        
    context['col'] = col

    return render(request, 'predicciones.html', context)

def download_pdf(request):
    rutaActual = os.path.abspath(os.getcwd())
    name = 'Reporte'
    with open(str(rutaActual) + '\\'+str(name)+'.csv', 'r') as file:
        file_data = file.read()
    response = HttpResponse(file_data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = "Reporte.csv"'
    return response

