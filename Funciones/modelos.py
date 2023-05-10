import pickle
import Funciones.sql_connection as sql
from numpy import isnan
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
import pandas as pd

import Funciones.ExportCsv as expcsv
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from datetime import datetime
import os

def datos_lab_filtros2(genero, edad_min, edad_max, fecha_ingreso_ini, fecha_ingreso_fin):
    conexion_db=sql.openDBconect(propiedadesUsuario = ["localhost", "root", "contra", "diagnostico_auto"])
    datos_mysql=sql.recolectar_labs2(conexion_db)
    sql.closeDBconect(conexion_db)

    df = datos_mysql

    if genero != '':
        df = df[df['genero'] == genero]
        
    if edad_min != '0' and edad_max != '0':
        df = df[df['edad'] >= int(edad_min)]
        df = df[df['edad'] <= int(edad_max)]
        
    if fecha_ingreso_ini != '' and fecha_ingreso_fin != '':
        fecha_ingreso_ini = pd.to_datetime(fecha_ingreso_ini, format='%Y-%m-%d')
        fecha_ingreso_fin = pd.to_datetime(fecha_ingreso_fin, format='%Y-%m-%d')

        df['fecha_ingreso'] = pd.to_datetime(df['fecha_ingreso'], format='%Y-%m-%d')

        df = df.loc[(df['fecha_ingreso'] >= fecha_ingreso_ini) & (df['fecha_ingreso'] < fecha_ingreso_fin)]

    return df

def datos_lab_filtros(genero, edad_min, edad_max, fecha_ingreso_ini, fecha_ingreso_fin):
    conexion_db=sql.openDBconect(propiedadesUsuario = ["localhost", "root", "contra", "diagnostico_auto"])
    datos_mysql=sql.recolectar_labs(conexion_db)
    sql.closeDBconect(conexion_db)

    df = datos_mysql
    col = []

    # summarize the number of rows with missing values for each column
    for i in range(df.shape[1]):
        # count number of rows with missing values
        n_miss = df.iloc[:, i].isnull().sum()
        perc = n_miss / df.shape[0] * 100
        if perc > 80.0:
            col.append(df.columns[i])

    for i in col:
        df.drop(i, axis = 1, inplace=True)

    y = pd.concat([df['edad'], df['genero'], df['fecha_ingreso']], axis=1)

    # Dataframe de nss pacientes
    NSS_pacientes = pd.concat([df['nss']], axis=1)


    X = df.drop('fecha_ingreso', axis=1)
    X = X.drop('edad', axis=1)
    X = X.drop('nss', axis = 1)
    X = X.drop('genero', axis = 1)
    X = X.drop('pres_arterial', axis = 1)

    # split into input and output elements
    data = X.values
    ix = [i for i in range(data.shape[1]) if i != 23]
    i, j = data[:, ix], data[:, 23]
    # print total missing
    print('Missing: %d' % sum(isnan(i).flatten()))
    # define imputer
    imputer = KNNImputer()
    # fit on the dataset
    imputer.fit(i)
    # transform the dataset
    Xtrans = imputer.transform(i)
    # print total missing
    print('Missing: %d' % sum(isnan(Xtrans).flatten()))

    Xtrans = pd.DataFrame(Xtrans)
    X = Xtrans

    df = pd.concat([X, y, NSS_pacientes], axis=1)

    if genero != '':
        df = df[df['genero'] == genero]
        
    if edad_min != '0' and edad_max != '0':
        df = df[df['edad'] >= int(edad_min)]
        df = df[df['edad'] <= int(edad_max)]
        
    if fecha_ingreso_ini != '' and fecha_ingreso_fin != '':
        fecha_ingreso_ini = pd.to_datetime(fecha_ingreso_ini, format='%Y-%m-%d')
        fecha_ingreso_fin = pd.to_datetime(fecha_ingreso_fin, format='%Y-%m-%d')

        df['fecha_ingreso'] = pd.to_datetime(df['fecha_ingreso'], format='%Y-%m-%d')

        df = df.loc[(df['fecha_ingreso'] >= fecha_ingreso_ini) & (df['fecha_ingreso'] < fecha_ingreso_fin)]

    #Drop de los nss
    NSS_pacientes = df['nss'].tolist()
    edad = df['edad'].tolist()
    gen = df['genero'].tolist()
    fecha = df['fecha_ingreso'].tolist()

    for i in range(len(fecha)):
        fecha[i] = str(fecha[i])

    NSS_pacientes = pd.DataFrame(NSS_pacientes, columns=['nss'])
    edad = pd.DataFrame(edad, columns=['edad'])
    gen = pd.DataFrame(gen, columns=['genero'])
    fecha = pd.DataFrame(fecha, columns=['fecha_ingreso'])
    NSS_pacientes = pd.concat([NSS_pacientes,edad,gen,fecha], axis=1)

    X = df.drop('edad', axis=1)
    X = X.drop('genero', axis=1)
    X = X.drop('fecha_ingreso', axis=1)
    X = X.drop('nss', axis=1)

    return X, NSS_pacientes


def KNN_3diag(X, NSS_pacientes, reporte):

    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\KNN_3diag.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'N_E_C'}, inplace = True)
    print('Termina proceso de hilo1')
    return reporte

def DT_3diag(X, NSS_pacientes, reporte):

    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\DT_3diag.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'N_E_C'}, inplace = True)
    print('Termina proceso de hilo1')
    return reporte

def MLP_3diag(X, NSS_pacientes, reporte):

    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\mlp_3_diag.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    ###reporte ['Diagnostico'] = reporte ['Diagnostico'].map({0 : 'control', 1 : 'embolia', 2 : 'neumonia'}).astype(str) #mapping numbers
    reporte.rename(columns = {'Diagnostico':'N_E_C'}, inplace = True)
    print('Termina proceso de hilo1')
    return reporte

def NB_3diag(X, NSS_pacientes, reporte):

    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\NB_control_embolia_neumonia.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'N_E_C'}, inplace = True)
    print('Termina proceso de hilo1')
    return reporte

def SVM_3diag(X, NSS_pacientes, reporte):

    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\SVM_control_neumonia_embolia_.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'N_E_C'}, inplace = True)
    print('Termina proceso de hilo1')
    return reporte

def KNN_N_E(X, NSS_pacientes, reporte):

    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\KNN_neumonia_embolia.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'N_E'}, inplace = True)
    print('Termina proceso de hilo2')
    return reporte

def DT_N_E(X, NSS_pacientes, reporte):

    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\DT_neumonia-embolia.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'N_E'}, inplace = True)
    print('Termina proceso de hilo2')
    return reporte

def MLP_N_E(X, NSS_pacientes, reporte):

    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\mlp_neumonia-embolia.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    ##reporte ['Diagnostico'] = reporte ['Diagnostico'].map({0 : 'control', 1 : 'embolia', 2 : 'neumonia'}).astype(str) #mapping numbers
    reporte.rename(columns = {'Diagnostico':'N_E'}, inplace = True)
    print('Termina proceso de hilo2')
    return reporte

def NB_N_E(X, NSS_pacientes, reporte):

    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\NB_embolia_neumonia.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'N_E'}, inplace = True)
    print('Termina proceso de hilo2')
    return reporte

def SVM_N_E(X, NSS_pacientes, reporte):

    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\SVM_neumonia_embolia.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'N_E'}, inplace = True)
    print('Termina proceso de hilo2')
    return reporte

def KNN_N_C(X, NSS_pacientes, reporte):
    
    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\KNN_neumonia_con.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'N_C'}, inplace = True)
    print('Termina proceso de hilo3')
    return reporte

def DT_N_C(X, NSS_pacientes, reporte):
    
    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\DT_neumonia-control.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'N_C'}, inplace = True)
    print('Termina proceso de hilo3')
    return reporte

def MLP_N_C(X, NSS_pacientes, reporte):
    
    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\mlp_neumonia-control.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    #reporte ['Diagnostico'] = reporte ['Diagnostico'].map({0 : 'control', 1 : 'embolia', 2 : 'neumonia'}).astype(str) #mapping numbers
    reporte.rename(columns = {'Diagnostico':'N_C'}, inplace = True)
    print('Termina proceso de hilo3')
    return reporte

def NB_N_C(X, NSS_pacientes, reporte):
    
    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\NB_control_neumonia.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'N_C'}, inplace = True)
    print('Termina proceso de hilo3')
    return reporte

def SVM_N_C(X, NSS_pacientes, reporte):
    
    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\SVM_neumonia_control.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'N_C'}, inplace = True)
    print('Termina proceso de hilo3')
    return reporte

def KNN_E_C(X, NSS_pacientes, reporte):
    
    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\KNN_embolia_con.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'E_C'}, inplace = True)
    print('Termina proceso de hilo4')
    return reporte

def DT_E_C(X, NSS_pacientes, reporte):
    
    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\DT_control-embolia.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'E_C'}, inplace = True)
    print('Termina proceso de hilo4')
    return reporte

def MLP_E_C(X, NSS_pacientes, reporte):
    
    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\mlp_control-embolia.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    #reporte ['Diagnostico'] = reporte ['Diagnostico'].map({0 : 'control', 1 : 'embolia', 2 : 'neumonia'}).astype(str) #mapping numbers
    reporte.rename(columns = {'Diagnostico':'E_C'}, inplace = True)
    print('Termina proceso de hilo4')
    return reporte

def NB_E_C(X, NSS_pacientes, reporte):
    
    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\NB_control_embolia.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'E_C'}, inplace = True)
    print('Termina proceso de hilo4')
    return reporte

def SVM_E_C(X, NSS_pacientes, reporte):
    
    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\SVM_embolia_control.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'E_C'}, inplace = True)
    print('Termina proceso de hilo4')
    return reporte

def KNN_N_O(X, NSS_pacientes, reporte):
    
    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\KNN_neumonia_otro.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'N_O'}, inplace = True)
    print('Termina proceso de hilo5')
    return reporte

def DT_N_O(X, NSS_pacientes, reporte):
    
    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\DT_N_O.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'N_O'}, inplace = True)
    print('Termina proceso de hilo5')
    return reporte

def MLP_N_O(X, NSS_pacientes, reporte):
    
    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\mlp_N_O.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'N_O'}, inplace = True)
    print('Termina proceso de hilo5')
    return reporte

def NB_N_O(X, NSS_pacientes, reporte):
    
    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\NB_N_O.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'N_O'}, inplace = True)
    print('Termina proceso de hilo5')
    return reporte

def SVM_N_O(X, NSS_pacientes, reporte):
    
    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\SVM_N_O.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'N_O'}, inplace = True)
    print('Termina proceso de hilo5')
    return reporte

def KNN_E_O(X, NSS_pacientes, reporte):
    
    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\KNN_embolia_otro.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'E_O'}, inplace = True)
    print('Termina proceso de hilo6')
    return reporte

def DT_E_O(X, NSS_pacientes, reporte):
    
    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\DT_E_O.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'E_O'}, inplace = True)
    print('Termina proceso de hilo6')
    return reporte

def MLP_E_O(X, NSS_pacientes, reporte):
    
    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\mlp_E_O.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'E_O'}, inplace = True)
    print('Termina proceso de hilo6')
    return reporte

def NB_E_O(X, NSS_pacientes, reporte):
    
    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\NB_E_O.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'E_O'}, inplace = True)
    print('Termina proceso de hilo6')
    return reporte

def SVM_E_O(X, NSS_pacientes, reporte):
    
    # load the model from disk
    rutaActual = os.path.abspath(os.getcwd())
    filename = rutaActual + '\\Funciones\\SVM_E_O.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    predictions = loaded_model.predict(X)

    predictions = pd.DataFrame(predictions, columns=['Diagnostico'])

    reporte2 = pd.concat([predictions, NSS_pacientes], axis=1)
    reporte = pd.concat([reporte,reporte2['Diagnostico']], axis=1)
    reporte.rename(columns = {'Diagnostico':'E_O'}, inplace = True)
    print('Termina proceso de hilo6')
    return reporte