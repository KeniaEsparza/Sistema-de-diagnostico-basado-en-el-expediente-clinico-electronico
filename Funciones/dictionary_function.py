def setDictNotasClinicas():
    resultado={}
    dictDefault= {
            'dx_inicial': '',
            'dx_final': '',
            'genero':'',
            'interrogatorio_inicial':'',
            'interrogatorio_final': '',
            'tokens_inicial':None,
            'tokens_final':None,
            'tokens_frec_inicial':None,
            'tokens_frec_final':None,
            'Biomedical_Cased_CBOW_inicial':None,
            'Biomedical_Cased_CBOW_final': None}

    resultado=dictDefault.copy()
    return (resultado)

def guardarDictNotasClinicas(datos,dic_default):
    resultado=None
    dic_general={}
    tuplaActual=None
    for i in range(len(datos[1])):
        dic_derivado = dic_default.copy()
        tuplaActual=datos[1][i]
        dic_derivado['dx_inicial']=tuplaActual[1]
        dic_derivado['dx_final']=tuplaActual[2]
        dic_derivado['genero']=tuplaActual[3]
        dic_derivado['interrogatorio_inicial']=tuplaActual[4]
        dic_derivado['interrogatorio_final']=tuplaActual[5]
        dic_general[int(tuplaActual[0])]=dic_derivado.copy()
        resultado=dic_general.copy()
    return resultado