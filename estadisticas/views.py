from django.shortcuts import render
from django.views.generic import TemplateView
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import Funciones.modelos as md
import numpy as np

import json
import pandas as pd
import os

import matplotlib.pyplot as plt
import io
import urllib, base64

def grafica_genero(df):
    gen = []
    lab = []
    val = df['genero'].value_counts()
    try:
        if val['f']:
            fem = val['f'] / len(df['genero'])
            gen.append(fem)
            lab.append('Femenino')
            
    except:
        print("An exception occurred")
    try:
        if val['m']:
            mas = val['m'] / len(df['genero'])
            gen.append(mas)
            lab.append('Masculino')
    except:
        print("An exception occurred")

    plt.pie(gen, labels=lab, labeldistance=1.15, autopct='%1.1f%%',wedgeprops = { 'linewidth' : 3, 'edgecolor' : 'white' })
    plt.title("Género")
    plt.style.use('ggplot')
    fig = plt.gcf()
    plt.close()
    return fig

def grafica_dig_inicial(df):
    val = df['diagnostico_inicial'].value_counts()
    diag=[]
    label=[]
    try:
        control = val['control'] / len(df['diagnostico_inicial'])
        diag.append(control)
        label.append('control')
    except:
        print("An exception occurred")
    try:
        neumonia = val['neumonia'] / len(df['diagnostico_inicial'])
        diag.append(neumonia)
        label.append('neumonia')
    except:
        print("An exception occurred")
    try:
        embolia = val['embolia'] / len(df['diagnostico_inicial'])
        diag.append(embolia)
        label.append('embolia')
    except:
        print("An exception occurred")
    plt.pie(diag, labels=label, labeldistance=1.15, autopct='%1.1f%%',wedgeprops = { 'linewidth' : 3, 'edgecolor' : 'white' })
    plt.title("Diagnostico inicial")
    plt.style.use('ggplot')
    fig = plt.gcf()
    plt.close()
    return fig

def grafica_dig_final(df):
    val = df['diagnostico_final'].value_counts()
    diag=[]
    label=[]
    try:
        control = val['control'] / len(df['diagnostico_final'])
        diag.append(control)
        label.append('control')
    except:
        print("An exception occurred")
    try:
        neumonia = val['neumonia'] / len(df['diagnostico_final'])
        diag.append(neumonia)
        label.append('neumonia')
    except:
        print("An exception occurred")
    try:
        embolia = val['embolia'] / len(df['diagnostico_final'])
        diag.append(embolia)
        label.append('embolia')
    except:
        print("An exception occurred")
    plt.pie(diag, labels=label, autopct='%1.1f%%',labeldistance=1.15, wedgeprops = { 'linewidth' : 3, 'edgecolor' : 'white' })
    plt.title("Diagnostico final")
    plt.style.use('ggplot')
    fig = plt.gcf()
    plt.close()
    return fig

def grafica_edad(df):
    try:
        df['edad'].plot.hist()
        plt.title("Edades")
        plt.xlabel("Rango de edades")
        plt.ylabel("Frecuencia")
        fig = plt.gcf()
        plt.close()
        return fig
    except:
        print("An exception ocurred")

def grafica_talla(df):
    try:
        df['talla'].plot.hist()
        plt.xlabel("Rango de tallas")
        plt.ylabel("Frecuencia")
        plt.title("Tallas")
        fig = plt.gcf()
        plt.close()
        return fig
    except:
        print("An exception ocurred")

def grafica_temperatura(df):
    try:
        df['temperatura'].plot.hist()
        plt.xlabel("Rango de temperaturas")
        plt.ylabel("Frecuencia")
        plt.title("Temperatura")
        fig = plt.gcf()
        plt.close()
        return fig
    except:
        print("An exception ocurred")

def grafica_frec_respiratoria(df):
    try:
        df['frec_respiratoria'].plot.hist()
        plt.title("Frecuencia Respiratoria")
        plt.xlabel("Rango de frecuencias respiratorias")
        plt.ylabel("Frecuencia")
        fig = plt.gcf()
        plt.close()
        return fig
    except:
        print("An exception ocurred")

def grafica_frec_cardiaca(df):
    try:
        df['frec_cardiaca'].plot.hist()
        plt.title("Frecuencia Cardíaca")
        plt.xlabel("Rango de frecuencias cardíacas")
        plt.ylabel("Frecuencia")
        fig = plt.gcf()
        plt.close()
        return fig
    except:
        print("An exception ocurred")

def grafica_imc(df):
    try:
        df['imc'].plot.hist()
        plt.xlabel("Rango de índice de masa corporal")
        plt.title("Índice de masa corporal")
        plt.ylabel("Frecuencia")
        fig = plt.gcf()
        plt.close()
        return fig
    except:
        print("An exception ocurred")

def grafica_saturacion(df):
    try:
        df['saturacion'].plot.hist()
        plt.xlabel("Rango de saturación")
        plt.title("Saturación")
        plt.ylabel("Frecuencia")
        fig = plt.gcf()
        plt.close()
        return fig
    except:
        print("An exception ocurred")

def grafica_glc_capilar(df):
    try:
        df['glc_capilar'].plot.hist()
        plt.xlabel("Rango de GLC capilar")
        plt.title("GLC capilar")
        plt.ylabel("Frecuencia")
        fig = plt.gcf()
        plt.close()
        return fig
    except:
        print("An exception ocurred")

def grafica_glucosa_sanguinea(df):
    try:
        df['glucosa sanguinea'].plot.hist()
        plt.title("Glucosa sanguínea")
        plt.xlabel("Rango de glucosa sanguínea")
        plt.ylabel("Frecuencia")
        fig = plt.gcf()
        plt.close()
        return fig
    except:
        print("An exception ocurred")

def grafica_magnesio(df):
    try:
        df['magnesio'].plot.hist()
        plt.title("Magnesio")
        plt.xlabel("Rango de magnesio")
        plt.ylabel("Frecuencia")
        fig = plt.gcf()
        plt.close()
        return fig
    except:
        print("An exception ocurred")

def grafica_potasio(df):
    try:
        df['potasio'].plot.hist()
        plt.title("Potasio")
        plt.xlabel("Rango de potasio")
        plt.ylabel("Frecuencia")
        fig = plt.gcf()
        plt.close()
        return fig
    except:
        print("An exception ocurred")

def grafica_calcio_serico(df):
    try:
        df['calcio serico'].plot.hist()
        plt.title("Calcio sérico")
        plt.xlabel("Rango de calcio sérico")
        plt.ylabel("Frecuencia")
        fig = plt.gcf()
        plt.close()
        return fig
    except:
        print("An exception ocurred")

def grafica_plaquetas(df):
    try:
        df['plaquetas'].plot.hist()
        plt.title("Plaquetas")
        plt.xlabel("Rango de plaquetas")
        plt.ylabel("Frecuencia")
        fig = plt.gcf()
        plt.close()
        return fig
    except:
        print("An exception ocurred")

def grafica_ccmh(df):
    try:
        df['ccmh'].plot.hist()
        plt.title("CCMH")
        plt.xlabel("Rango de CCMH")
        plt.ylabel("Frecuencia")
        fig = plt.gcf()
        plt.close()
        return fig
    except:
        print("An exception ocurred")

def get_plt(fig):
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    image_png = buf.getvalue()
    string = base64.b64encode(image_png)
    string = string.decode('utf-8')
    buf.close()
    return string


def HomePageView(request):
    template = loader.get_template('estadisticas.html')
    context = {}
    return HttpResponse(template.render(context,request))

def filtros(request):
    template = loader.get_template('filtros_graficas.html')
    context = {}
    return HttpResponse(template.render(context,request))

def res_graficos(request):
    genero = request.POST['genero']
    edad_min = request.POST['edad_min']
    edad_max = request.POST['edad_max']
    fecha_ingreso_ini = request.POST['fecha_ingreso_ini']
    fecha_ingreso_fin = request.POST['fecha_ingreso_fin']
    demograficas = request.POST.get('demograficas', False)
    clinicas = request.POST.get('clinicas', False)
    laboratorios = request.POST.get('laboratorios', False)
    df = md.datos_lab_filtros2(genero, edad_min, edad_max, fecha_ingreso_ini, fecha_ingreso_fin)
    
    context = {}
    
    if demograficas == 'on':
        try:
            fig = grafica_genero(df)
            genero = get_plt(fig)
            context['genero'] = genero
        except:
            ("an exception ocurred")
        try:
            fig2 = grafica_dig_inicial(df)
            diag = get_plt(fig2)
            context['diag'] = diag
        except:
            ("an exception ocurred")
        try:
            fig3 = grafica_dig_final(df)
            diagf = get_plt(fig3)
            context['diagf'] = diagf
        except:
            ("an exception ocurred")
        try:
            fig4 = grafica_edad(df)
            edad = get_plt(fig4)
            context['edad'] = edad
        except:
            ("an exception ocurred")
        try:
            fig5 = grafica_talla(df)
            talla = get_plt(fig5)
            context['talla'] = talla
        except:
            ("an exception ocurred")
        
    if clinicas == 'on':
        try:
            fig6 = grafica_temperatura(df)
            temperatura = get_plt(fig6)
            context['temperatura'] = temperatura
        except:
            ("an exception ocurred")
        try:
            fig7 = grafica_frec_respiratoria(df)
            frec_respiratoria = get_plt(fig7)
            context['frec_respiratoria'] = frec_respiratoria
        except:
            ("an exception ocurred")
        try:
            fig8 = grafica_frec_cardiaca(df)
            frec_cardiaca = get_plt(fig8)
            context['frec_cardiaca'] = frec_cardiaca
        except:
            ("an exception ocurred")
        try:
            fig9 = grafica_saturacion(df)
            saturacion = get_plt(fig9)
            context['saturacion'] = saturacion
        except:
            ("an exception ocurred")

        try:
            fig10 = grafica_imc(df)
            imc = get_plt(fig10)
            context['imc'] = imc
        except:
            ("An exception ocurred")
        try:
            fig11 = grafica_glc_capilar(df)
            glc_capilar = get_plt(fig11)
            context['glc_capilar'] = glc_capilar
        except:
            ("an exception ocurred")
    
    if laboratorios == 'on':
        try:
            fig12 = grafica_glucosa_sanguinea(df)
            glucosa_sanguinea = get_plt(fig12)
            context['glucosa_sanguinea'] = glucosa_sanguinea
        except:
            ("an exception ocurred")
        try:
            fig13 = grafica_magnesio(df)
            magnesio = get_plt(fig13)
            context['magnesio'] = magnesio
        except:
            ("an exception ocurred")
        try:
            fig14 = grafica_potasio(df)
            potasio = get_plt(fig14)
            context['potasio'] = potasio
        except:
            ("an exception ocurred")
        try:
            fig15 = grafica_calcio_serico(df)
            calcio_serico = get_plt(fig15)
            context['calcio_serico'] = calcio_serico
        except:
            ("an exception ocurred")
        try:
            fig16 = grafica_plaquetas(df)
            plaquetas = get_plt(fig16)
            context['plaquetas'] = plaquetas
        except:
            ("an exception ocurred")
        try:
            fig17 = grafica_ccmh(df)
            ccmh = get_plt(fig17)
            context['ccmh'] = ccmh
        except:
            ("an exception ocurred")
    
    return render(request,'graficas.html',context)