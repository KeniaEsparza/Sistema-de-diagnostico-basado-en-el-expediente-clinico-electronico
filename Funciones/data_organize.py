import re
import sys
import pandas as pd
import numpy as np
import os

from sklearn.impute import KNNImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler    #Normalizacion Z-Score https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html

import Funciones.ExportCsv as expcsv

def strToint(valor):
    resultado=None

    try:
        valor = re.sub('(\w+\.\w+)\.\w+', '\\1', valor)
    except:
        print('\n\tError con la estructura (2 puntos) de la variable')

    try:
        valor = re.sub('(\w+|\w+\.\w+)\/\w+\.*\w*', '\\1', valor)
    except:
        print('\n\tError con la estructura (diagonal) de la variable')

    try:
        valor = float(valor)
    except:
        print('\n\tError al convertir la variable a float')

    resultado=valor
    return resultado

def organizar_datos_IO(lista_diccionarios,name_tec,test_size):
    resultado=[]
    diccionario_biomedical_WE_cased=lista_diccionarios

    df = pd.DataFrame(data=diccionario_biomedical_WE_cased)
    serie_dx_final=df.loc["dx_final"]
    #Array de token
    serie_Biomedical_cased_CBOW_final=df.loc[name_tec]

    #determina el array mas grande
    max_length_cbow_final=0
    for array in serie_Biomedical_cased_CBOW_final:
        if len(array)>max_length_cbow_final: max_length_cbow_final=len(array)

    input_biomedical_cased_CBOW_final = np.zeros((serie_Biomedical_cased_CBOW_final.shape[0], max_length_cbow_final))
    n = 0

    for array in serie_Biomedical_cased_CBOW_final:
        #Tamaño faltante
        concatZeros=max_length_cbow_final-len(array)
        npzeros=np.zeros(concatZeros,dtype=np.float32)
        #que dato quiere convertir a flotante
        nparray=np.array((array), dtype=np.float32)
        nparrayzeros= np.hstack((nparray, npzeros))
        input_biomedical_cased_CBOW_final[n]=nparrayzeros
        n+=1
    del n

    input_dx_final = serie_dx_final.values
    target_label = LabelEncoder()
    target = target_label.fit_transform(input_dx_final)

    X = input_biomedical_cased_CBOW_final
    y = target

    resultado = [X, y]

    if test_size>1:
        test_size=test_size/100

    ###???????
    X_model, X_prueba, y_model, y_prueba = train_test_split(X, y, test_size = test_size, random_state = 42)
    resultado=[X, y, X_model, y_model, X_prueba, y_prueba]
    return resultado

def OrganizeGroupData_IO(lista_diccionarios,name_tec,test_size):
    resultado = []
    diccionario_biomedical_WE_cased = lista_diccionarios

    df = pd.DataFrame(data=diccionario_biomedical_WE_cased)
    serie_dx_final = df.loc["dx_final"]
    serie_Biomedical_cased_CBOW_final = df.loc[name_tec]

    max_length_cbow_final = 0
    for array in serie_Biomedical_cased_CBOW_final:
        if len(array) > max_length_cbow_final: max_length_cbow_final = len(array)

    input_biomedical_cased_CBOW_final = np.zeros((serie_Biomedical_cased_CBOW_final.shape[0], max_length_cbow_final))
    n = 0
    for array in serie_Biomedical_cased_CBOW_final:
        concatZeros = max_length_cbow_final - len(array)
        npzeros = np.zeros(concatZeros, dtype=np.float32)
        nparray = np.array((array), dtype=np.float32)
        nparrayzeros = np.hstack((nparray, npzeros))
        input_biomedical_cased_CBOW_final[n] = nparrayzeros
        n += 1
    del n

    input_dx_final = serie_dx_final.values
    target_label = LabelEncoder()
    targetall = target_label.fit_transform(input_dx_final)

    #Juntar Label por grupos (enfermedades=1+2; otrosE=0+1; otrosN=0+2) donde control=0,embo=1 y neumo=2
    targetEnf = []
    targetotrosE = []
    targetotrosN = []
    for label in targetall:
        if label == 0:
            targetEnf.append(0)
            targetotrosE.append(1)
            targetotrosN.append(1)
        elif label==1:
            targetEnf.append(1)
            targetotrosE.append(0)
            targetotrosN.append(1)
        elif label==2:
            targetEnf.append(1)
            targetotrosE.append(1)
            targetotrosN.append(0)

    targetEnf = np.array(targetEnf)
    targetotrosE = np.array(targetotrosE)
    targetotrosN = np.array(targetotrosN)


    # ELIMINAR COLUMNA 0 de input_biomedical_cased_CBOW_final por tener valor igual en todas las columnas: 0.01587927 = actual
    input_biomedical_cased_CBOW_final=np.delete(input_biomedical_cased_CBOW_final, obj=0, axis=1)

    Xall = input_biomedical_cased_CBOW_final
    yall = targetall
    yC_Enf=targetEnf
    yE_otros=targetotrosE
    yN_otros=targetotrosN

    #Juntar arrays X+Y y eliminar grupos extras
    dfAll = pd.DataFrame(data=Xall)
    dfAll['target'] = yall

    dfCE=dfAll.copy()
    dfCN=dfAll.copy()
    dfEN=dfAll.copy()

    dfCE.drop(dfCE[dfCE['target'] == 2].index, inplace=True)
    dfCN.drop(dfCN[dfCN['target'] == 1].index, inplace=True)
    dfEN.drop(dfEN[dfEN['target'] == 0].index, inplace=True)

    yCE = dfCE["target"].to_numpy()
    yCN = dfCN["target"].to_numpy()
    yEN = dfEN["target"].to_numpy()

    yCE = target_label.fit_transform(yCE)
    yCN = target_label.fit_transform(yCN)
    yEN = target_label.fit_transform(yEN)

    dfCE.drop('target',axis='columns', inplace=True)
    dfCN.drop('target',axis='columns', inplace=True)
    dfEN.drop('target',axis='columns', inplace=True)

    XCE=dfCE.to_numpy()
    XCN=dfCN.to_numpy()
    XEN=dfEN.to_numpy()

    if test_size > 1:
        test_size = test_size / 100

    #GRUPO ALL (3 elementos)
    Xall_model, Xall_prueba, yall_model, yall_prueba = train_test_split(Xall, yall, test_size=test_size, random_state=42)
    grupoALL = [Xall, yall, Xall_model, yall_model, Xall_prueba, yall_prueba]

    #GRUPO Control Vs Enfemedades
    XC_Enf_model, XC_Enf_prueba, yC_Enf_model, yC_Enf_prueba = train_test_split(Xall, yC_Enf, test_size=test_size, random_state=42)
    grupoC_Enf = [Xall, yC_Enf, XC_Enf_model, yC_Enf_model, XC_Enf_prueba, yC_Enf_prueba]

    #GRUPO Embolia Vs Otros
    XE_otros_model, XE_otros_prueba, yE_otros_model, yE_otros_prueba = train_test_split(Xall, yE_otros, test_size=test_size, random_state=42)
    grupoE_Otros = [Xall, yE_otros, XE_otros_model, yE_otros_model, XE_otros_prueba, yE_otros_prueba]

    #GRUPO Neumonia Vs Otros
    XN_otros_model, XN_otros_prueba, yN_otros_model, yN_otros_prueba = train_test_split(Xall, yN_otros, test_size=test_size, random_state=42)
    grupoN_otros = [Xall, yN_otros, XN_otros_model, yN_otros_model, XN_otros_prueba, yN_otros_prueba]

    #GRUPO control Vs embolia
    XCE_model, XCE_prueba, yCE_model, yCE_prueba = train_test_split(XCE, yCE, test_size=test_size, random_state=42)
    grupoCE = [XCE, yCE, XCE_model, yCE_model, XCE_prueba, yCE_prueba]

    #GRUPO control Vs neumonia
    XCN_model, XCN_prueba, yCN_model, yCN_prueba = train_test_split(XCN, yCN, test_size=test_size, random_state=42)
    grupoCN = [XCN, yCN, XCN_model, yCN_model, XCN_prueba, yCN_prueba]

    #GRUPO embolia Vs neumonia
    XEN_model, XEN_prueba, yEN_model, yEN_prueba = train_test_split(XEN, yEN, test_size=test_size, random_state=42)
    grupoEN = [XEN, yEN, XEN_model, yEN_model, XEN_prueba, yEN_prueba]



    resultado=[grupoALL,grupoC_Enf,grupoE_Otros,grupoN_otros,grupoCE,grupoCN,grupoEN]
    return resultado

def structure_study_data_frame(extracted_data,listaDeterminacion):
    resultado=[]
    listDict=[]
    listDictFinal=[]
    listFolioDict=[]
    dictResult={}
    TuplaInstancias=None
    resultadoINT = None
    valorKey=extracted_data[0]
    valorInstancias=extracted_data[1]
    extendValorKey=[]

    #DataFrame en Blanco******************************************************************************
    extendValorKey=valorKey.copy()
    extendValorKey.extend(listaDeterminacion)

    df= pd.DataFrame(columns=extendValorKey)
    #*************************************************************************************************
    for valor in extendValorKey:
        dictResult[str(valor)]=None

    for valor in valorInstancias:
        TuplaInstancias=valor
        for iteracion in range(len(TuplaInstancias)):
            if valorKey[iteracion]=='resultado':
                resultadoINT=strToint(TuplaInstancias[iteracion])
                dictResult[str(valorKey[iteracion])] = resultadoINT
                dictResult[str(TuplaInstancias[iteracion-1])]=resultadoINT
                resultadoINT=None
            else:
                dictResult[str(valorKey[iteracion])] = TuplaInstancias[iteracion]

        listDict.append(dictResult.copy())
        dictResult = dictResult.fromkeys(dictResult, None)

    for i in range(len(listDict)):
        dictResult=listDict[i]
        folioDict=dictResult['folio_orden']
        for dict in listDict:
            if dict['folio_orden']==folioDict:
                dictResult[dict['determinacion']]=dict['resultado']

        if not folioDict in listFolioDict:
            listFolioDict.append(folioDict)
            listDictFinal.append(dictResult.copy())
        dictResult = dictResult.fromkeys(dictResult, None)

    for i in range(len(listDictFinal)):
        x = 0
        for key, value in listDictFinal[i].items():
            x += 1

        df = df.append(listDictFinal[i], ignore_index=True, sort=False)

    df=df.drop(columns=['determinacion', 'resultado'])

    # Mover Columna DataFrame al final
    column_size = len(df.columns) - 1
    name_column = 'fecha_ingreso'
    move_column = df.pop(name_column)

    df.insert(column_size, name_column, move_column)

    # Mover Columna DataFrame al final
    column_size = len(df.columns) - 1
    name_column = 'edad'
    move_column = df.pop(name_column)

    df.insert(column_size, name_column, move_column)

    # Ordenar filas de menor a mayor con respecto a la columna "orden"
    df = df.sort_values(by=['nss'])

    # Verificacion de valores duplicados en columna 'orden'
    #dfDupli=df.duplicated(subset=['nss'], keep=False)

    # agrupamiento de valores repetidos donde se selecciona el maximo valor
    df2 = df.drop(columns=['folio_orden'])

    try:
        #df2 = df2.groupby('nss').max()
        df2 = df2.groupby('nss',group_keys=True,dropna=False).min().reset_index()
    except OSError as err:
        print("\tOS error: {0}".format(err))
    except ValueError as e:
        print("\tERROR con el agrupamiento de datos\n\t".upper(), e)
    except:
        print("\tUnexpected error:", sys.exc_info()[0])
        raise

    resultado=df2
    return resultado

def preprosLabs(df):
    #merge columnas con mismo nombre pero con espacios al final
    for col_name in df.columns:
        text = col_name.replace(' ', '')
        df = df.rename(columns={str(col_name): str(text)})

    df = df.groupby(level=0, axis=1).first()

    tmpDF = pd.DataFrame(columns=['p_art_sistolica', 'p_art_diastolica'])
    tmpDF[['p_art_sistolica', 'p_art_diastolica']] = df['pres_arterial'].str.split('/', expand=True)
    df = pd.concat([df, tmpDF], axis=1)

    position = df.columns.get_loc('pres_arterial') + 1
    name_column = 'p_art_diastolica'
    move_column = df.pop(name_column)
    df.insert(position, name_column, move_column)

    name_column = 'p_art_sistolica'
    move_column = df.pop(name_column)
    df.insert(position, name_column, move_column)

    df = df.drop('pres_arterial', axis=1)

    position = len(df.columns)-1
    name_column = 'diagnostico_final'
    move_column = df.pop(name_column)
    df.insert(position, name_column, move_column)

    position = 0
    name_column = 'nss'
    move_column = df.pop(name_column)
    df.insert(position, name_column, move_column)

    #discretizar columna de genero en 0 y 1
    label_conv = LabelEncoder()
    tag = label_conv.fit_transform(df.loc[:, "genero"])
    df1 = df.drop('genero', axis=1)
    df1.insert(1, 'genero', tag)

    #eliminacion del 65% de datos faltantes
    df1 = df1.loc[:, df1.isnull().sum() < 0.65 * df1.shape[0]]

    ##SEGREGACION DE ATRIBUTOS CON CORRELACION DE PEARSON >=90%

    #generar datos faltantes mediante metodo de KNN
    index_nss = df1['nss'].tolist()
    index_nss=list(map(int, index_nss))
    df1 = df1.drop('nss', axis=1)

    dx_final=df1['diagnostico_final'].to_numpy()
    df1 = df1.drop('diagnostico_final', axis=1)
    df_dxFinal=pd.DataFrame(data=dx_final,index=index_nss ,columns=['diagnostico_final'])

    head = []
    for col_name in df1.columns:
        head.append(col_name)

    imputer = KNNImputer(n_neighbors=2, weights="uniform")
    npdf1 = imputer.fit_transform(df1)

    df2 = pd.DataFrame(data=npdf1,index=index_nss ,columns=head)
    df3 = pd.concat([df2, df_dxFinal], axis=1)

    #estandarizar y normalizar todos los datos.
    df_sklearn = df3.copy()

    #estandarizar Z-score
    for col_name in df_sklearn.columns:
        if (str(col_name) != 'diagnostico_final') and (str(col_name) != 'genero'):
            data = np.array(df_sklearn[col_name]).reshape(-1, 1)
            scaler = StandardScaler()
            scaler.fit(data)
            df_sklearn[col_name] = scaler.transform(data)
        else: None

    
    #Normalizar
    for col_name in df_sklearn.columns:
        if str(col_name) != 'diagnostico_final':
            df_sklearn[col_name] = MinMaxScaler().fit_transform(np.array(df_sklearn[col_name]).reshape(-1, 1))
        else: None

    resultado=df_sklearn
    return resultado


def joinWELabs_IO(lista_diccionarios,df_labs,name_tec,test_size):
    resultado = []
    labs=df_labs.copy()
    diccionario_biomedical_WE_cased = lista_diccionarios

    df = pd.DataFrame(data=diccionario_biomedical_WE_cased)
    index_df=df.columns
    serie_dx_final = df.loc["dx_final"]
    serie_Biomedical_cased_CBOW_final = df.loc[name_tec]

    max_length_cbow_final = 0
    for array in serie_Biomedical_cased_CBOW_final:
        if len(array) > max_length_cbow_final: max_length_cbow_final = len(array)

    input_biomedical_cased_CBOW_final = np.zeros((serie_Biomedical_cased_CBOW_final.shape[0], max_length_cbow_final))
    n = 0
    for array in serie_Biomedical_cased_CBOW_final:
        concatZeros = max_length_cbow_final - len(array)
        npzeros = np.zeros(concatZeros, dtype=np.float32)
        nparray = np.array((array), dtype=np.float32)
        nparrayzeros = np.hstack((nparray, npzeros))
        input_biomedical_cased_CBOW_final[n] = nparrayzeros
        n += 1
    del n

    input_dx_final = serie_dx_final.values
    target_label = LabelEncoder()
    targetall = target_label.fit_transform(input_dx_final)

    # ELIMINAR COLUMNA 0 de input_biomedical_cased_CBOW_final por tener valor igual en todas las columnas: 0.01587927 = actual
    input_biomedical_cased_CBOW_final = np.delete(input_biomedical_cased_CBOW_final, obj=0, axis=1)

    Xall = input_biomedical_cased_CBOW_final
    yall = targetall

    #Crear dataframe de notas clinicas
    dfAll = pd.DataFrame(data=Xall,index=index_df)
    dfYAll= pd.DataFrame(data=yall,index=index_df,columns=['target'])

    #Unir dataframes de notas clinicas con labs
    labs = labs.drop('diagnostico_final', axis=1)

    dfjoin=dfAll.join(labs)
    dfjoin = pd.concat([dfjoin, dfYAll], axis=1)
    dfjoin = dfjoin.dropna()

    #Division de dataframe por grupos target
    dfXAll = dfjoin.copy()
    yall = dfXAll["target"].to_numpy()
    yall = target_label.fit_transform(yall)
    dfXAll.drop('target', axis='columns', inplace=True)
    Xall=dfXAll.to_numpy()

    #Juntar Label por grupos (enfermedades=1+2; otrosE=0+1; otrosN=0+2) donde control=0,embo=1 y neumo=2    ***********
    targetEnf = []
    targetotrosE = []
    targetotrosN = []
    for label in yall:
        if label == 0:
            targetEnf.append(0)
            targetotrosE.append(1)
            targetotrosN.append(1)
        elif label==1:
            targetEnf.append(1)
            targetotrosE.append(0)
            targetotrosN.append(1)
        elif label==2:
            targetEnf.append(1)
            targetotrosE.append(1)
            targetotrosN.append(0)

    targetEnf = np.array(targetEnf)
    targetotrosE = np.array(targetotrosE)
    targetotrosN = np.array(targetotrosN)

    yC_Enf=targetEnf
    yE_otros=targetotrosE
    yN_otros=targetotrosN
    #*******************************************************************************************************************

    dfCE = dfjoin.copy()
    dfCN = dfjoin.copy()
    dfEN = dfjoin.copy()

    dfCE.drop(dfCE[dfCE['target'] == 2].index, inplace=True)
    dfCN.drop(dfCN[dfCN['target'] == 1].index, inplace=True)
    dfEN.drop(dfEN[dfEN['target'] == 0].index, inplace=True)

    yCE = dfCE["target"].to_numpy()
    yCN = dfCN["target"].to_numpy()
    yEN = dfEN["target"].to_numpy()

    yCE = target_label.fit_transform(yCE)
    yCN = target_label.fit_transform(yCN)
    yEN = target_label.fit_transform(yEN)

    dfCE.drop('target', axis='columns', inplace=True)
    dfCN.drop('target', axis='columns', inplace=True)
    dfEN.drop('target', axis='columns', inplace=True)

    XCE = dfCE.to_numpy()
    XCN = dfCN.to_numpy()
    XEN = dfEN.to_numpy()

    #EXPORTAR DATAFRAME a .CSV
    expcsv.exportCsvLabs(dfjoin, 'DFGeneral')

    #Crear entradas a redes neuronales
    if test_size > 1:
        test_size = test_size / 100

    #GRUPO ALL (3 elementos)
    Xall_model, Xall_prueba, yall_model, yall_prueba = train_test_split(Xall, yall, test_size=test_size, random_state=42)
    grupoALL = [Xall, yall, Xall_model, yall_model, Xall_prueba, yall_prueba]

    #GRUPO Control Vs Enfemedades
    XC_Enf_model, XC_Enf_prueba, yC_Enf_model, yC_Enf_prueba = train_test_split(Xall, yC_Enf, test_size=test_size, random_state=42)
    grupoC_Enf = [Xall, yC_Enf, XC_Enf_model, yC_Enf_model, XC_Enf_prueba, yC_Enf_prueba]

    #GRUPO Embolia Vs Otros
    XE_otros_model, XE_otros_prueba, yE_otros_model, yE_otros_prueba = train_test_split(Xall, yE_otros, test_size=test_size, random_state=42)
    grupoE_Otros = [Xall, yE_otros, XE_otros_model, yE_otros_model, XE_otros_prueba, yE_otros_prueba]

    #GRUPO Neumonia Vs Otros
    XN_otros_model, XN_otros_prueba, yN_otros_model, yN_otros_prueba = train_test_split(Xall, yN_otros, test_size=test_size, random_state=42)
    grupoN_otros = [Xall, yN_otros, XN_otros_model, yN_otros_model, XN_otros_prueba, yN_otros_prueba]

    #GRUPO control Vs embolia
    XCE_model, XCE_prueba, yCE_model, yCE_prueba = train_test_split(XCE, yCE, test_size=test_size, random_state=42)
    grupoCE = [XCE, yCE, XCE_model, yCE_model, XCE_prueba, yCE_prueba]

    #GRUPO control Vs neumonia
    XCN_model, XCN_prueba, yCN_model, yCN_prueba = train_test_split(XCN, yCN, test_size=test_size, random_state=42)
    grupoCN = [XCN, yCN, XCN_model, yCN_model, XCN_prueba, yCN_prueba]

    #GRUPO embolia Vs neumonia
    XEN_model, XEN_prueba, yEN_model, yEN_prueba = train_test_split(XEN, yEN, test_size=test_size, random_state=42)
    grupoEN = [XEN, yEN, XEN_model, yEN_model, XEN_prueba, yEN_prueba]



    resultado=[grupoALL,grupoC_Enf,grupoE_Otros,grupoN_otros,grupoCE,grupoCN,grupoEN]


    return resultado

def structure_study_data_frame2(extracted_data,listaDeterminacion):
    resultado=[]
    listDict=[]
    listDictFinal=[]
    listFolioDict=[]
    dictResult={}
    TuplaInstancias=None
    resultadoINT = None
    valorKey=extracted_data[0]
    valorInstancias=extracted_data[1]
    extendValorKey=[]

    #DataFrame en Blanco******************************************************************************
    extendValorKey=valorKey.copy()
    extendValorKey.extend(listaDeterminacion)

    df= pd.DataFrame(columns=extendValorKey)
    #*************************************************************************************************
    for valor in extendValorKey:
        dictResult[str(valor)]=None

    for valor in valorInstancias:
        TuplaInstancias=valor
        for iteracion in range(len(TuplaInstancias)):
            if valorKey[iteracion]=='resultado':
                resultadoINT=strToint(TuplaInstancias[iteracion])
                dictResult[str(valorKey[iteracion])] = resultadoINT
                dictResult[str(TuplaInstancias[iteracion-1])]=resultadoINT
                resultadoINT=None
            else:
                dictResult[str(valorKey[iteracion])] = TuplaInstancias[iteracion]

        listDict.append(dictResult.copy())
        dictResult = dictResult.fromkeys(dictResult, None)

    for i in range(len(listDict)):
        dictResult=listDict[i]
        folioDict=dictResult['folio_orden']
        for dict in listDict:
            if dict['folio_orden']==folioDict:
                dictResult[dict['determinacion']]=dict['resultado']

        if not folioDict in listFolioDict:
            listFolioDict.append(folioDict)
            listDictFinal.append(dictResult.copy())
        dictResult = dictResult.fromkeys(dictResult, None)

    for i in range(len(listDictFinal)):
        x = 0
        for key, value in listDictFinal[i].items():
            x += 1

        df = df.append(listDictFinal[i], ignore_index=True, sort=False)

    df=df.drop(columns=['determinacion', 'resultado'])
    # Mover Columna DataFrame al final
    column_size = len(df.columns) - 1
    name_column = 'fecha_ingreso'
    move_column = df.pop(name_column)

    df.insert(column_size, name_column, move_column)


    # Mover Columna DataFrame al final
    column_size = len(df.columns) - 1
    name_column = 'edad'
    move_column = df.pop(name_column)

    df.insert(column_size, name_column, move_column)

    # Mover Columna DataFrame al final
    column_size = len(df.columns) - 1
    name_column = 'diagnostico_inicial'
    move_column = df.pop(name_column)

    df.insert(column_size, name_column, move_column)

    # Mover Columna DataFrame al final
    column_size = len(df.columns) - 1
    name_column = 'diagnostico_final'
    move_column = df.pop(name_column)

    df.insert(column_size, name_column, move_column)

    # Ordenar filas de menor a mayor con respecto a la columna "orden"
    df = df.sort_values(by=['nss'])

    # Verificacion de valores duplicados en columna 'orden'
    #dfDupli=df.duplicated(subset=['nss'], keep=False)

    # agrupamiento de valores repetidos donde se selecciona el maximo valor
    df2 = df.drop(columns=['folio_orden'])

    try:
        #df2 = df2.groupby('nss').max()
        df2 = df2.groupby('nss',group_keys=True,dropna=False).min().reset_index()
        df2 = df2.sort_values(by=['diagnostico_final'])
    except OSError as err:
        print("\tOS error: {0}".format(err))
    except ValueError as e:
        print("\tERROR con el agrupamiento de datos\n\t".upper(), e)
    except:
        print("\tUnexpected error:", sys.exc_info()[0])
        raise

    resultado=df2
    return resultado