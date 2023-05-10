import os
import re
import pickle

def rutasCarpetas():
    resultado=[]
    contenidoFile = []
    contenidoFileEgreso = []
    rutaFileEgreso=""

    listRutasGenerales=[]
    listRutasClinicalFiles=[]
    listrutasClinicalEgreso=[]


    rutaActual = os.path.abspath(os.getcwd())
    listRutasGenerales.append(rutaActual)

    rutaActual = str(rutaActual)+"\\DatosClinicos"
    listRutasGenerales.append(rutaActual)
    contenidoFile = os.listdir(str(listRutasGenerales[1]))

    for filesName in contenidoFile:
        rutaActual = str(listRutasGenerales[1])+"\\"+str(filesName)
        listRutasClinicalFiles.append(rutaActual)
        #captura de carpetas existentes en carpeta de EGRESO (Diagnostico Final)
        nameEgreso= re.search("Egreso", filesName)
        if nameEgreso:
            nameEgreso= str(nameEgreso.group())
            rutaFileEgreso = str(rutaActual)
            contenidoFileEgreso=os.listdir(rutaFileEgreso)


    for filesName in contenidoFileEgreso:
        rutaActual = str(rutaFileEgreso) + "\\" + str(filesName)
        listrutasClinicalEgreso.append(rutaActual)

    resultado.append(listRutasGenerales)
    resultado.append(listRutasClinicalFiles)
    resultado.append(listrutasClinicalEgreso)

    return resultado

def codesCIE10(rutaOrigen):
    resultado=[]
    rutaTxt=str(rutaOrigen)+'\\TextFiles\\CodigosCie10.txt'

    file = open(str(rutaTxt), 'r')
    codesText = file.read()
    codesText = str(codesText)
    file.close()

    codesText = codesText.replace('\r', '').replace('\n', '')
    codesText=codesText.lower()
    TxtSplit = re.split(r'embolia:|control:', codesText, 2)

    for i in range(len(TxtSplit)):
        SearchTxt = re.findall(r"([a-zA-Z]\d\d\w)", TxtSplit[i])
        resultado.append(SearchTxt)
    return (resultado)

#Guardado de valores de diccionario en pickle
def pickleGuardarDic(diccionario,Nombre):
    rutaArchivo='PickleFiles\\dic_'+str(Nombre)+'.pickle'
    file= open(str(rutaArchivo),'wb')
    pickle.dump(diccionario, file)
    file.close()
    return None

#Cargardo de valores de pickle a diccionario
def pickleCargarDic(rutaOrigen):
    resultado={}
    ruta=str(rutaOrigen)+'\\PickleFiles'

    contenido = os.listdir(ruta)

    #Evaluacion de archivos Pickles existentes
    for fichero in contenido:
        if os.path.isfile(os.path.join(ruta, fichero)) and fichero.endswith('.pickle'):

            tipoDocPickle = re.search("\_.+\.", fichero)
            tipoDocPickle = str(tipoDocPickle.group())
            tipoDocPickle=tipoDocPickle.replace('_','').replace('.','')

            file= open(str(ruta)+'\\'+str(fichero),'rb')
            #locals()["Dic_" + str(tipoDocPickle)] = pickle.load(file)          #Guarda variables locales con nombres variante
            resultado["Dic_" + str(tipoDocPickle)] = pickle.load(file)
            file.close()
    return resultado

#Estructuras de notas clinicas (para extraccion de datos en pdf)        ************************************************
def estructuraNotaInicial(NotaControl):
    resultado=[]
    textoBuscado=''
    textoDelimitador=''
    FormatoBuscado=''
    valorDiccionario=''
    listaTextoBuscado=[]
    listaFormatoBuscado=[]
    listaTextoDelimitador=[]
    listaValorDiccionario=[]

    textoBuscado="Fecha de Clasificacion:"
    textoDelimitador=''
    FormatoBuscado='\d+\/\d+\/\d+'
    valorDiccionario='fecha_ingreso'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))


    textoBuscado="Especialidad:"
    textoDelimitador='\sNombre|\sResidente'
    FormatoBuscado='[a-z]+\s*[a-z]*'
    FormatoDelimitador=str(FormatoBuscado)+'\sNombre|'+str(FormatoBuscado)+'\sResidente'
    valorDiccionario='especialidad_ingreso'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    FormatoDelimitador=FormatoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    if not NotaControl:
        textoBuscado="\\nMOTIVO DE LA CONSULTA"
        textoDelimitador='RESUMEN DEL INTERROGATORIO'
        FormatoBuscado='.+\s*'
        valorDiccionario='motivo_consulta'
        textoBuscado=textoBuscado.lower()
        textoDelimitador=textoDelimitador.lower()
        listaTextoBuscado.append(textoBuscado)
        listaTextoDelimitador.append(str(textoDelimitador))
        listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
        listaValorDiccionario.append(str(valorDiccionario))

        textoBuscado="\\nRESUMEN DEL INTERROGATORIO"
        textoDelimitador='DIAGNOSTICOS O PROBLEMAS CLINICOS'
        FormatoBuscado='.+\s*'
        valorDiccionario='interrogatorio'
        textoBuscado=textoBuscado.lower()
        textoDelimitador=textoDelimitador.lower()
        listaTextoBuscado.append(textoBuscado)
        listaTextoDelimitador.append(str(textoDelimitador))
        listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
        listaValorDiccionario.append(str(valorDiccionario))

        textoBuscado = "\\nDIAGNOSTICOS O PROBLEMAS CLINICOS"
        textoDelimitador = 'PLAN DE TRATAMIENTO'
        FormatoBuscado = '.+\s*'
        valorDiccionario = 'diagnostico'
        textoBuscado = textoBuscado.lower()
        textoDelimitador = textoDelimitador.lower()
        listaTextoBuscado.append(textoBuscado)
        listaTextoDelimitador.append(str(textoDelimitador))
        listaFormatoBuscado.append(str(FormatoBuscado) + str(textoDelimitador))
        listaValorDiccionario.append(str(valorDiccionario))

        textoBuscado = '\\nINDICACIONES'
        textoDelimitador = ''
        FormatoBuscado = '.+\s*'
        valorDiccionario = 'indicaciones'
        textoBuscado = textoBuscado.lower()
        textoDelimitador = textoDelimitador.lower()
        listaTextoBuscado.append(textoBuscado)
        listaTextoDelimitador.append(str(textoDelimitador))
        listaFormatoBuscado.append(str(FormatoBuscado) + str(textoDelimitador))
        listaValorDiccionario.append(str(valorDiccionario))

    else:
        textoBuscado="\\nANTECEDENTES HEREDO-FAMILIARES"
        textoDelimitador='DIAGNOSTICO'
        FormatoBuscado='.+\s*'
        valorDiccionario='interrogatorio'
        textoBuscado=textoBuscado.lower()
        textoDelimitador=textoDelimitador.lower()
        listaTextoBuscado.append(textoBuscado)
        listaTextoDelimitador.append(str(textoDelimitador))
        listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
        listaValorDiccionario.append(str(valorDiccionario))

        textoBuscado = "\\nDIAGNOSTICO"
        textoDelimitador = 'PLAN DE TRATAMIENTO'
        FormatoBuscado = '.+\s*'
        valorDiccionario = 'diagnostico'
        textoBuscado = textoBuscado.lower()
        textoDelimitador = textoDelimitador.lower()
        listaTextoBuscado.append(textoBuscado)
        listaTextoDelimitador.append(str(textoDelimitador))
        listaFormatoBuscado.append(str(FormatoBuscado) + str(textoDelimitador))
        listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado='\\nPLAN DE TRATAMIENTO'
    textoDelimitador='PRONOSTICO'
    FormatoBuscado='.+\s*'
    valorDiccionario='plan_tratamiento'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado='\\nPRONOSTICO'
    textoDelimitador='INDICACIONES'
    FormatoBuscado='.+\s*'
    valorDiccionario='pronostico'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador)+'|'+str(FormatoBuscado))
    listaValorDiccionario.append(str(valorDiccionario))

    #signos vitales ----------------------------------------------------------------------------------
    textoBuscado='\\nEstado de Salud:'
    textoDelimitador=''
    FormatoBuscado='[a-z]+'
    valorDiccionario='estado_salud'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado='\\nPeso:'
    textoDelimitador=''
    FormatoBuscado='^\s\d\d\d*\.\d|^\s\d\d\d*|^\d\d\d*\.\d|^\d\d\d*'
    valorDiccionario='peso'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado='\\nTalla:'
    textoDelimitador=''
    FormatoBuscado='^\s\d\d\d\.\d|^\s\d\d\d|^\d\d\d\.\d|^\d\d\d'
    valorDiccionario='talla'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado='\\nTemperatura:'
    textoDelimitador=''
    FormatoBuscado='^\s\d\d\.\d|^\s\d\d|^\d\d\.\d|^\d\d'
    valorDiccionario='temperatura'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado='\\nFrecuencia Respiratoria:'
    textoDelimitador=''
    FormatoBuscado='^\s\d\d\.\d|^\s\d\d|^\d\d\.\d|^\d\d'
    valorDiccionario='frec_respiratoria'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado='\\nFrecuencia Cardiaca:'
    textoDelimitador=''
    FormatoBuscado='^\s\d\d\d*\.\d|^\s\d\d\d*|^\d\d\d*\.\d|^\d\d\d*'
    valorDiccionario='frec_cardiaca'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado='\\nTension Arterial:'
    textoDelimitador=''
    FormatoBuscado='^\s\d\d\d*\/\d\d*\d*|^\d\d\d*/\d\d*\d*'
    valorDiccionario='pres_arterial'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado='\\nIndice Masa Corporal:'
    textoDelimitador=''
    FormatoBuscado='^\s\d\d\d*\.\d\d*|^\s\d\d\d*|^\d\d\d*\.\d\d*|^\d\d\d*'
    valorDiccionario='imc'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado='\\nSaturacion:'
    textoDelimitador=''
    FormatoBuscado='^\s\d\d\d*\.\d\d*|^\s\d\d\d*|^\d\d\d*\.\d\d*|^\d\d\d*'
    valorDiccionario='saturacion'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado='\\nGlucosa Capilar:'
    textoDelimitador=''
    FormatoBuscado='^\s\d\d\d*\.\d\d*|^\s\d\d\d*|^\d\d\d*\.\d\d*|^\d\d\d*'
    valorDiccionario='glc_capilar'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    resultado.append(listaTextoBuscado)
    resultado.append(listaTextoDelimitador)
    resultado.append(listaFormatoBuscado)
    resultado.append(listaValorDiccionario)
    return resultado

#Estadar inicial de diccionarios para notas clinicas                    ************************************************
def setDictNotaInicial():
    resultado={}
    dictDefault= {'nss': '',
            'fecha_ingreso': '',
            'genero':'',
            'especialidad_ingreso': None,
            'motivo_consulta':None,
            'interrogatorio': None,
            'diagnostico':None,
            'plan_tratamiento': None,
            'pronostico': None,
            'indicaciones': None,
            'estado_salud': None,
            'peso': None,
            'talla': None,
            'temperatura': None,
            'frec_respiratoria': None,
            'frec_cardiaca': None,
            'pres_arterial': None,
            'imc': None,
            'saturacion': None,
            'glc_capilar': None,
            'diagnostico_inicial':None}


    resultado=dictDefault
    return (resultado)

#Estructuras de Laboratorios (para extraccion de datos en pdf)          ************************************************
def estructuraLaboratorio():
    resultado=[]
    listFormatoLabGeneral=[]
    listFormatoLabValores=[]

    formatoNSS='\nnss\s*\:*\s*(\d+\s*\d+\s*\d+)'
    formatoFolioOrden='\nfolio\s*de\s*la\s*orden\:*\s*(\d+)'
    formatoFechaOrden='\nfecha\s*de\s*la\s*orden\:*\s*(\d+\/\d+\/\d+)'
    formatoEdad='\nedad\:*\s*(\d+)'
    formatoServicioSolicita='\sservicio\ssolicitante\:\s*(.+)'

    listFormatoLabGeneral.append(formatoNSS)
    listFormatoLabGeneral.append(formatoFolioOrden)
    listFormatoLabGeneral.append(formatoFechaOrden)
    listFormatoLabGeneral.append(formatoEdad)
    listFormatoLabGeneral.append(formatoServicioSolicita)

    formatoDeterminacion ='\@[a-z]+ó*\:*\s*\.*\,*\/*\-*\%*\(*[a-z]*\)*[a-z]*\:*\s*\.*\,*\/*\-*\%*\(*[a-z]*\)*[a-z]*\:*\s*\.*\,*\/*\-*\%*\(*[a-z]*\)*'\
                            '[a-z]*\:*\s*\.*\,*\/*\-*\%*\(*[a-z]*\)*[a-z]*\:*\s*\.*\,*\/*\-*\%*\(*[a-z]*\)*[a-z]*\:*\s*\.*\,*\/*\-*\%*\d*\(*[a-z]*\)*'\
                            '[a-z]*\:*\%*\s\-*\d'
    formatoResultados = '\s\-*\d+\.*\d*\s|\s\d+\.*\d*\/\d+\.*\d*\s'
    formatoUnidades='\d\s\w+\/*\w*\:*\d*\.*\d*\s*\(|\d\s\%\s*\(|\d\s\%\s*/ál\s*\('
    formatoValoresNormales = '\s\(.+\)'

    listFormatoLabValores.append(formatoDeterminacion)
    listFormatoLabValores.append(formatoResultados)
    listFormatoLabValores.append(formatoUnidades)
    listFormatoLabValores.append(formatoValoresNormales)

    resultado.append(listFormatoLabGeneral)
    resultado.append(listFormatoLabValores)
    return resultado

#Estadar inicial de diccionarios para laboratorios                      ************************************************
def setDictLaboratorio():
    resultado=[]
    dictDefault = {'nss': '',
                   'folio_orden': '',
                   'fecha_orden': None,
                   'edad': None,
                   'servicio_solicita': None,
                   'estudios': None}

    dictEstudios={}

    dictLabValores = {'determinacion': None, 'resultados': None, 'unidades': None, 'valores_normales': None}

    resultado.append(dictDefault)
    resultado.append(dictEstudios)
    resultado.append(dictLabValores)
    return resultado

#Estadar inicial de diccionarios para notas de Egreso                    ************************************************
def setDictNotaFinal():
    resultado={}
    dictDefault= {'nss': '',
            'fecha_ingreso': '',
            'fecha_egreso': '',
            'especialidad_egreso': None,
            'motivo_egreso':None,
            'envio':None,
            'diagnostico_ingreso':None,
            'diagnostico_egreso':None,
            'resumen_evolucion': None,
            'problemas_pendientes': None,
            'plan_tratamiento': None,
            'recomendaciones': None,
            'factores_riesgo': None,
            'pronostico': None,
            'diagnostico_defuncion': None,
            'estado_salud': None,
            'peso': None,
            'talla': None,
            'temperatura': None,
            'frec_respiratoria': None,
            'frec_cardiaca': None,
            'pres_arterial': None,
            'imc': None,
            'saturacion': None,
            'glc_capilar': None,
            'diagnostico_final': None}

    resultado=dictDefault
    return (resultado)

#Estructuras de notas clinicas (para extraccion de datos en pdf)        ************************************************
def estructuraNotaFinal():
    resultado=[]
    textoBuscado=''
    textoDelimitador=''
    FormatoBuscado=''
    valorDiccionario=''
    FormatoDelimitador=''
    listaTextoBuscado=[]
    listaFormatoBuscado=[]
    listaTextoDelimitador=[]
    listaValorDiccionario=[]

    textoBuscado="Fecha de Clasificacion:"
    textoDelimitador=''
    FormatoBuscado='\d+\/\d+\/\d+'
    valorDiccionario='fecha_egreso'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado="Especialidad:"
    textoDelimitador='\sNombre|\sResidente'
    FormatoBuscado='[a-z]+\s*[a-z]*'
    FormatoDelimitador=str(FormatoBuscado)+'\sNombre|'+str(FormatoBuscado)+'\sResidente'
    valorDiccionario='especialidad_egreso'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    FormatoDelimitador=FormatoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado="\\nFECHA DE INGRESO"
    textoDelimitador=''
    FormatoBuscado='\d+\/\d+\/\d+'
    valorDiccionario='fecha_ingreso'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado="\\nMOTIVO DE EGRESO\\s*\\n"
    textoDelimitador='ENVIO A'
    FormatoBuscado='.+\s*'
    valorDiccionario='motivo_egreso'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado="\\nENVIO A\\s*\\n"
    textoDelimitador='DIAGNOSTICOS DE INGRESO|\:'
    FormatoBuscado='.+\s*'
    FormatoDelimitador=str(FormatoBuscado)+'DIAGNOSTICOS DE INGRESO|'+str(FormatoBuscado)+':'
    valorDiccionario='envio'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    FormatoDelimitador=FormatoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(FormatoDelimitador)
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado="\\nDIAGNOSTICOS DE INGRESO\\s*\\n"
    textoDelimitador='DIAGNOSTICOS DE EGRESO'
    FormatoBuscado='.+\s*'
    valorDiccionario='diagnostico_ingreso'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado="\\nDIAGNOSTICOS DE EGRESO\\s*\\n"
    textoDelimitador='RESUMEN DE EVOLUCION'
    FormatoBuscado='.+\s*'
    valorDiccionario='diagnostico_egreso'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado="\\nRESUMEN DE EVOLUCION, MANEJO DURANTE LA ESTANCIA HOSPITALARIA Y\\s*\\n"
    textoDelimitador='PROBLEMAS CLINICOS PENDIENTES|PLAN DE MANEJO Y TRATAMIENTO|DIAGNOSTICOS DE DEFUNCION'
    FormatoBuscado='.+\s*'
    FormatoDelimitador=str(FormatoBuscado)+'PROBLEMAS CLINICOS PENDIENTES|'+str(FormatoBuscado)+'PLAN DE MANEJO Y TRATAMIENTO|'+str(FormatoBuscado)+'DIAGNOSTICOS DE DEFUNCION|'+str(FormatoBuscado)
    valorDiccionario='resumen_evolucion'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    FormatoDelimitador=FormatoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(FormatoDelimitador)
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado="\\nPROBLEMAS CLINICOS PENDIENTES\\s*\\n"
    textoDelimitador='PLAN DE MANEJO Y TRATAMIENTO'
    FormatoBuscado='.+\s*'
    valorDiccionario='problemas_pendientes'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado="\\nPLAN DE MANEJO Y TRATAMIENTO\\s*\\n"
    textoDelimitador='RECOMENDACIONES PARA VIGILANCIA AMBULATORIA|ATENCION DE FACTORES DE RIESGO'
    FormatoBuscado='.+\s*'
    FormatoDelimitador=str(FormatoBuscado)+'RECOMENDACIONES PARA VIGILANCIA AMBULATORIA|'+str(FormatoBuscado)+'ATENCION DE FACTORES DE RIESGO|'+str(FormatoBuscado)
    valorDiccionario='plan_tratamiento'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    FormatoDelimitador=FormatoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(FormatoDelimitador)
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado="\\nRECOMENDACIONES PARA VIGILANCIA AMBULATORIA\\s*\\n"
    textoDelimitador='ATENCION DE FACTORES DE RIESGO|PRONOSTICO'
    FormatoBuscado='.+\s*'
    FormatoDelimitador = str(FormatoBuscado)+'ATENCION DE FACTORES DE RIESGO|'+str(FormatoBuscado)+'PRONOSTICO'
    valorDiccionario='recomendaciones'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    FormatoDelimitador=FormatoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(FormatoDelimitador)
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado="\\nATENCION DE FACTORES DE RIESGO\\s*\\n"
    textoDelimitador='PRONOSTICO'
    FormatoBuscado='.+\s*'
    valorDiccionario='factores_riesgo'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado = '\\nPRONOSTICO\\s*\\n'
    textoDelimitador = ''
    FormatoBuscado = '.+\s*'
    valorDiccionario = 'pronostico'
    textoBuscado = textoBuscado.lower()
    textoDelimitador = textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado) + str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado = '\\nDIAGNOSTICOS DE DEFUNCION\\s*\\n'
    textoDelimitador = ''
    FormatoBuscado = '.+\s*'
    valorDiccionario = 'diagnostico_defuncion'
    textoBuscado = textoBuscado.lower()
    textoDelimitador = textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado) + str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    #signos vitales ----------------------------------------------------------------------------------
    textoBuscado='\\nEstado de Salud:'
    textoDelimitador=''
    FormatoBuscado='[a-z]+'
    valorDiccionario='estado_salud'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado='\\nPeso:'
    textoDelimitador=''
    FormatoBuscado='^\s\d\d\d*\.\d|^\s\d\d\d*|^\d\d\d*\.\d|^\d\d\d*'
    valorDiccionario='peso'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado='\\nTalla:'
    textoDelimitador=''
    FormatoBuscado='^\s\d\d\d\.\d|^\s\d\d\d|^\d\d\d\.\d|^\d\d\d'
    valorDiccionario='talla'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado='\\nTemperatura:'
    textoDelimitador=''
    FormatoBuscado='^\s\d\d\.\d|^\s\d\d|^\d\d\.\d|^\d\d'
    valorDiccionario='temperatura'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado='\\nFrecuencia Respiratoria:'
    textoDelimitador=''
    FormatoBuscado='^\s\d\d\.\d|^\s\d\d|^\d\d\.\d|^\d\d'
    valorDiccionario='frec_respiratoria'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado='\\nFrecuencia Cardiaca:'
    textoDelimitador=''
    FormatoBuscado='^\s\d\d\d*\.\d|^\s\d\d\d*|^\d\d\d*\.\d|^\d\d\d*'
    valorDiccionario='frec_cardiaca'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado='\\nTension Arterial:'
    textoDelimitador=''
    FormatoBuscado='^\s\d\d\d*\/\d\d*\d*|^\d\d\d*/\d\d*\d*'
    valorDiccionario='pres_arterial'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado='\\nIndice Masa Corporal:'
    textoDelimitador=''
    FormatoBuscado='^\s\d\d\d*\.\d\d*|^\s\d\d\d*|^\d\d\d*\.\d\d*|^\d\d\d*'
    valorDiccionario='imc'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado='\\nSaturacion:'
    textoDelimitador=''
    FormatoBuscado='^\s\d\d\d*\.\d\d*|^\s\d\d\d*|^\d\d\d*\.\d\d*|^\d\d\d*'
    valorDiccionario='saturacion'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    textoBuscado='\\nGlucosa Capilar:'
    textoDelimitador=''
    FormatoBuscado='^\s\d\d\d*\.\d\d*|^\s\d\d\d*|^\d\d\d*\.\d\d*|^\d\d\d*'
    valorDiccionario='glc_capilar'
    textoBuscado=textoBuscado.lower()
    textoDelimitador=textoDelimitador.lower()
    listaTextoBuscado.append(textoBuscado)
    listaTextoDelimitador.append(str(textoDelimitador))
    listaFormatoBuscado.append(str(FormatoBuscado)+str(textoDelimitador))
    listaValorDiccionario.append(str(valorDiccionario))

    resultado.append(listaTextoBuscado)
    resultado.append(listaTextoDelimitador)
    resultado.append(listaFormatoBuscado)
    resultado.append(listaValorDiccionario)
    return resultado