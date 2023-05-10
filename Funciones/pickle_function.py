import pickle

#Guardado de diccionario en pickle
def pickleSaveDic(diccionario):
    file= open('PickleFiles\\dic_notas.pickle','wb')
    pickle.dump(diccionario, file)
    file.close()
    return None

def pickleSaveDicVect(diccionario):
    file= open('PickleFiles\\dic_notas_vector.pickle','wb')
    pickle.dump(diccionario, file)
    file.close()
    return None

def pickleSaveBiomedicalCasedWE(lista_diccionarios):
    diccionario_biomedical_WE_cased=lista_diccionarios[0]
    resumen_biomedical_WE_cased=lista_diccionarios[1]

    file= open('PickleFiles\\dic_Biomedical_WE_Cased.pickle','wb')
    pickle.dump(diccionario_biomedical_WE_cased, file)
    file.close()

    file= open('PickleFiles\\res_Biomedical_WE_Cased.pickle','wb')
    pickle.dump(resumen_biomedical_WE_cased, file)
    file.close()
    return None

def pickleSaveParamDic(diccionario,we):
    file= open('PickleFiles\\dic_set_param_'+str(we)+'.pickle','wb')
    pickle.dump(diccionario, file)
    file.close()
    return None

def pickleSaveResultDic(diccionario,we):
    file= open('PickleFiles\\dic_result_param_'+str(we)+'.pickle','wb')
    pickle.dump(diccionario, file)
    file.close()
    return None

#Cargado de diccionario de pickle
def pickleCargarDic():
    resultado={}
    try:
        file = open('PickleFiles\\dic_notas.pickle', 'rb')
        resultado= pickle.load(file)
        file.close()
    except:
        print('\n\tNo existe archivo pickle a cargar'.upper())
    return resultado

def pickleCargarDicVect():
    resultado={}
    try:
        file = open('PickleFiles\\dic_notas_vector.pickle', 'rb')
        resultado= pickle.load(file)
        file.close()
    except:
        print('\n\tNo existe archivo pickle a cargar'.upper())
    return resultado

def pickleLoadBiomedicalCasedWE():
    resultado=[]
    diccionario_biomedical_WE_cased = {}
    resumen_biomedical_WE_cased = {}

    try:
        file = open('PickleFiles\\dic_Biomedical_WE_Cased.pickle', 'rb')
        diccionario_biomedical_WE_cased= pickle.load(file)
        file.close()
    except:
        print('\n\tNo existe archivo pickle a cargar'.upper())

    try:
        file = open('PickleFiles\\res_Biomedical_WE_Cased.pickle', 'rb')
        resumen_biomedical_WE_cased= pickle.load(file)
        file.close()
    except:
        print('\n\tNo existe archivo pickle a cargar'.upper())

    resultado.append(diccionario_biomedical_WE_cased)
    resultado.append(resumen_biomedical_WE_cased)
    return resultado