import os
import pandas as pd
import numpy as np

def createDf (data):
    resultado=None
    keysDic=[]
    dicNSS=data[0]

    for key in dicNSS.keys():
        keysDic.append(key)

    arrKeys = np.array(keysDic)

    df = pd.DataFrame(data=data[0])

    #Target------------------------------------------------------
    dx_final=df.loc['dx_final']
    target = dx_final.values
    #input_dx_final = dx_final.values
    #target_label = LabelEncoder()
    #target = target_label.fit_transform(input_dx_final)
    #---------------------------------------------------------

    df_WE_start=df.loc['Biomedical_Cased_CBOW_inicial']
    df_WE_final=df.loc['Biomedical_Cased_CBOW_final']

    #DATA FRAME DE INTERROGATORIOS FINALES.---------------------
    length_final = 0
    for array in df_WE_final:
        if len(array) > length_final: length_final = len(array)

    arrayFinal = np.zeros((df_WE_final.shape[0], length_final))
    n = 0

    for array in df_WE_final:
        concatZeros = length_final - len(array)
        npzeros = np.zeros(concatZeros, dtype=np.float32)
        nparray = np.array((array), dtype=np.float32)
        nparrayzeros = np.hstack((nparray, npzeros))
        arrayFinal[n] = nparrayzeros
        n += 1
    del n, concatZeros, npzeros, nparray, nparrayzeros


    dfFinal = pd.DataFrame(arrayFinal,
                           index=arrKeys)
    dfFinal['target']=target
    #----------------------------------------------------------

    # DATA FRAME DE INTERROGATORIOS INICIALES.---------------------
    length_start = 0
    for array in df_WE_start:
        if len(array) > length_start: length_start = len(array)

    arrayStart = np.zeros((df_WE_start.shape[0], length_start))
    n = 0

    for array in df_WE_start:
        concatZeros = length_start - len(array)
        npzeros = np.zeros(concatZeros, dtype=np.float32)
        nparray = np.array((array), dtype=np.float32)
        nparrayzeros = np.hstack((nparray, npzeros))
        arrayStart[n] = nparrayzeros
        n += 1
    del n, concatZeros, npzeros, nparray, nparrayzeros

    dfStart = pd.DataFrame(arrayStart,
                           index=arrKeys)
    dfStart['target']=target

    resultado=[dfStart,dfFinal]
    return resultado

def exportCsv(dic):
    resultado=None
    data=createDf(dic)

    dfStart=data[0]
    dfFinal=data[1]

    resultado = None

    rutaActual = os.path.abspath(os.getcwd())

    dfStart.to_csv(str(rutaActual) + '\\ArchivosCSV\\notasIniciales.csv', index=True, header=False)
    dfFinal.to_csv(str(rutaActual) + '\\ArchivosCSV\\notasFinales.csv', index=True, header=False)

    return resultado


def exportCsvLabs(df,name):
    rutaActual = os.path.abspath(os.getcwd())
    df.to_csv(str(rutaActual) + '\\'+str(name)+'.csv', index=True, header=True)
    return None

def importCsvLabs():
    resultado=None
    rutaActual = os.path.abspath(os.getcwd())
    nameFile=str(rutaActual) + '\\ArchivosCSV\\LabsPreprocesados.csv'
    df = pd.read_csv(nameFile,index_col=0)

    resultado=df.copy()
    return resultado