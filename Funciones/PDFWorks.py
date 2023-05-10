import os
import re
import datetime
import Funciones.PDFSupports as soportFuntions
import pdfplumber

from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import resolve1

#extracion de datos para creacion de diccionario de pdfs---------------
def extraccionPDFNotaInicial(rutaPDF,diccEstandar):
    resultado=[]
    NotaControl=False
    pagesText=""
    text=""
    NumPages=None
    textSplit=[]
    errorDate=False
    txtSearch=''
    txtGenero=''

    textPage=[]

    rutaActual = os.path.abspath(os.getcwd())

    errorExtracionNSS=''

    # llamar lista de codigos formato txt
    CodigosCIE = soportFuntions.codesCIE10(rutaActual)
    CodeNeumonia = CodigosCIE[0]
    CodeEmbolia = CodigosCIE[1]
    CodeControl = CodigosCIE[2]  # Añadido Control 12/06/2021

    # Lectura y obtencion de texto de PDFs con pdfminer   ***************************
    output_string = StringIO()
    with open(str(rutaPDF), 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
        NumPages=resolve1(doc.catalog['Pages'])['Count']

    text=output_string.getvalue()
    text=text.lower()

    # Revision del texto extraido para pruebas ________________________________________
    f = open(str(rutaActual)+'\\TextFiles\\pdfMiner0.txt', 'w+')
    f.write(str(text))
    f.close()
    #__________________________________________________________________________________
    text = text.replace('\n ', ' ')
    text = text.replace('\n\n\n', '\n').replace('\n\n', '\n')
    text = text.replace('   ', ' ').replace('  ', ' ')

    try:
        textSplit=re.split('\n\x0c',text)
    except:
        print('\n\tNo hay paginas para separar'.upper())

    if len(textSplit)>1:
        text=str(textSplit[0])
        # QUITAR ENCABEZADOS
        for numPagina in range(1,len(textSplit)):
            textoSinEncabezado = None

            try:
                tablaExtra=re.search('triage y nota inicial del servicio de urgencias', str(textSplit[numPagina]))
                tablaExtra=tablaExtra.group(0)
                break;
            except: None

            try:
                textoSinEncabezado = re.sub('instituto mexicano.+\n(.+\n)+\d+\/\d+\/\d+\s\-\s\d+\:\d+\n*', '', str(textSplit[numPagina]))
                text = str(text) + str(textoSinEncabezado)
            except: None



    textSplit=[]

    # Revision del texto extraido para pruebas ________________________________________
    f = open(str(rutaActual) + '\\TextFiles\\pdfMiner1.txt', 'w+')
    f.write(str(text))
    f.close()
    # __________________________________________________________________________________
    text = text.replace('\x0c', '')

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Revision del texto extraido para pruebas ________________________________________
    f = open(str(rutaActual)+'\\TextFiles\\pdfMiner2.txt', 'w+')
    f.write(str(text))
    f.close()
    #__________________________________________________________________________________
    #DETECTAR GENERO Y GUARDAR VALOR.....12/05/2021
    try:
        txtGenero = re.search('agregado m.dico:\s*\d(\w)\d', text)
        txtGenero = txtGenero.group(1)

        diccEstandar['genero'] = str(txtGenero)
    except:
        print('\n\t\tError con buscar el genero...'.upper())

    #LIMPIAR TEXTO "text" de simbolos y apocrofes 11/06/2021
    try:
        text = text.replace('á', 'a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
        text = text.replace('à', 'a').replace('è','e').replace('ì','i').replace('ò','o').replace('ù','u')
        text = text.replace('*', '').replace('!', '').replace('¡', '').replace('?', '').replace('¿', '')
    except:
        print('\n\t\ttexto actualmente limpio'.upper())

    # Revision del texto extraido para pruebas ________________________________________
    f = open(str(rutaActual)+'\\TextFiles\\pdfMiner3.txt', 'w+')
    f.write(str(text))
    f.close()
    #__________________________________________________________________________________


    #DETECTAR SI SE TRATA DE NOTA INICIAL DE URGENCIA o CONTROL
    try:
        txtSearch = re.search('especialidad:\s*(\w+)', text)
        txtSearch = txtSearch.group(1)
    except:
        print('\n\t\tError con buscar la especialidad...'.upper())

    if txtSearch=='cirugia':
        NotaControl = True
    elif txtSearch=='oncologia':
        NotaControl = True
    elif txtSearch=='gastroenterologia':
        NotaControl = True
    elif txtSearch=='endocrinologia':
        NotaControl = True
    else:
        NotaControl = False


    if NotaControl:
        diccEstandar['motivo_consulta'] = 'control cirugía bariátrica'
        diccEstandar['diagnostico_inicial'] = 'control'


    listaBusquedaNotaInicial = soportFuntions.estructuraNotaInicial(NotaControl)

    listTextoBuscado=listaBusquedaNotaInicial[0]
    listaTextoDelimitador=listaBusquedaNotaInicial[1]
    listFormatoBuscado=listaBusquedaNotaInicial[2]
    listaValorDiccionario=listaBusquedaNotaInicial[3]

    if len(listTextoBuscado) == len(listFormatoBuscado):
        sizeList = len(listTextoBuscado)

    for iterador in range(sizeList):
        TextSplit = []
        TextSplit = re.split(str(listTextoBuscado[iterador]), str(text), 2)

        #AGREGAR ACONDCIONAMIENTO DE TEXTO text=text.replace('\n', '')
        for numSplit in range(len(TextSplit)):
            TextSplit[numSplit] = TextSplit[numSplit].replace('\n', ' ')
            TextSplit[numSplit] = TextSplit[numSplit].replace('   ', ' ').replace('  ', ' ')

        if len(TextSplit) > 1:
            reSearch = re.findall(str(listFormatoBuscado[iterador]), str(TextSplit[1]))

            if not reSearch:
                reSearch = None
            elif listaTextoDelimitador[iterador] != '':
                reSearch = re.split(str(listaTextoDelimitador[iterador]), str(reSearch[0]), 2)
                reSearch = reSearch[0]
            else:
                reSearch = reSearch[0]
        else:
            reSearch = None

        if reSearch:
            reSearch=re.sub('^\s*', '', reSearch)
            reSearch = re.sub('$\s*', '', reSearch)
        #agregar eliminacion de espacio al final del string

        if reSearch: print('Valor encontrado: '.upper() + reSearch)
        else: print('Valor encontrado: '.upper() + "NULL")

        # DETECTAR CAMPO DIAGNOSTICO INICIAL    12/06/2021
        try:
            if listTextoBuscado[iterador]=="\\nDIAGNOSTICOS O PROBLEMAS CLINICOS".lower() and NotaControl==False:
                diccEstandar['diagnostico_inicial'] = 'otro'

                # Deteccion de codigos de "EGRESO"
                SearchCodeIngreso = re.findall(r"[a-zA-Z]\d\d\w", str(reSearch))

                for i in SearchCodeIngreso:
                    for j in CodeNeumonia:
                        if j == i:
                            diccEstandar['diagnostico_inicial'] = 'neumonia'
                            break

                for i in SearchCodeIngreso:
                    for j in CodeEmbolia:
                        if j == i:
                            diccEstandar['diagnostico_inicial'] = 'embolia'
                            break
            else:None
        except:
            print('\n\tError con deteccion de diagnostico'.upper())


        #DETECTAR SI TEXTO ES FECHA
        # Try Catch por falla de lectura en apartado "fecha de clasificacion"
        try:
            if listTextoBuscado[iterador]=="Fecha de Clasificacion:".lower():
                #Conversion a formato YYYY-MM-DD
                reSearch= datetime.datetime.strptime(reSearch, '%d/%m/%Y')
            else:None
        except:
            errorDate=True


        #CASO PARA CUANDO reSearch pueda convertirse de str a decimal
        try:
            reSearch=float(reSearch)
        except:
            pass

        # Agregar valor reSearch a diccionario
        diccEstandar[str(listaValorDiccionario[iterador])] = reSearch

        #Try Catch por falla de lectura en apartado "Resumen del Interrogatorio"
        if ((str(listTextoBuscado[iterador]))=="RESUMEN DEL INTERROGATORIO".lower()) and (reSearch==None):
            errorExtracionNSS=(str(diccEstandar['nss']))

        elif errorDate:
            errorExtracionNSS=(str(diccEstandar['nss']))

    resultado.append(diccEstandar.copy())
    resultado.append(errorExtracionNSS)

    return resultado

def extraccionPDFLaboratorio(rutaPDF,listFormatos,listDiccionario):
    resultado=[]
    errorExtracionNSS = ''
    stringDeterminacionSustituto = ''
    listEstudiosLabs = []

    formatoNSS = str(listFormatos[0][0])
    formatoFolioOrden = str(listFormatos[0][1])
    formatoFechaOrden = str(listFormatos[0][2])
    formatoEdad = str(listFormatos[0][3])
    formatoServicioSolicita = str(listFormatos[0][4])

    formatoDeterminacion = str(listFormatos[1][0])
    formatoResultados = str(listFormatos[1][1])
    formatoUnidades = str(listFormatos[1][2])
    formatoValoresNormales = str(listFormatos[1][3])

    dictGeneral=listDiccionario[0]
    dictEstudios=listDiccionario[1]
    dictValoresEstudios=listDiccionario[2]

    rutaOrigen = os.path.abspath(os.getcwd())

    NSSactual=dictGeneral['nss']

    #EXTRACION DE TEXTO DEL PDF LAB     ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    pagesText=''
    text=''
    textSplit=''

    # Lectura y obtencion de texto de PDFs con PDFPlumber   **************************
    PDFfile = pdfplumber.open(rutaPDF)
    for page in PDFfile.pages:
        page_content = page.extract_text()
        pagesText = pagesText + page_content
        pagesText=pagesText.lower()
        #Quitar encabezado de labs y mensaje de biomarcador---------------------------
        try:
            pagesText = re.sub('fecha\sde\simpre.+\n+(.+\n)+resultados\svalidados\n', '', pagesText)
        except:
            print('\n\tOK: No se encontro condicion para sustitucion')

        try:
            pagesText = re.sub('este\sbiomarcador.+\n+(.+\n)+\.\.\.\..+\s*\n', '', pagesText)
        except:
            print('\n\tOK: No se encontro condicion para sustitucion')

        try:
            pagesText = re.sub('este biomarcador.+\n(.+\n)+aqui emitidas\n', '', pagesText)
        except:
            print('\n\tOK: No se encontro condicion para sustitucion')
        #-----------------------------------------------------------------------------

    PDFfile.close()
    text = pagesText.lower()

    # Revision del texto extraido para pruebas ________________________________________
    f = open(str(rutaOrigen)+'\\TextFiles\\txtLaboratorio0.txt', 'w+')
    f.write(str(text))
    f.close()
    #__________________________________________________________________________________
    text = re.sub('\n\s+', '\n', text)
    text= text.replace(' ', '@')
    text=re.sub('@+', ' ', text)

    #**********************************************************************************

    # Revision del texto extraido para pruebas ________________________________________
    f = open(str(rutaOrigen)+'\\TextFiles\\txtLaboratorio1.txt', 'w+')
    f.write(str(text))
    f.close()
    #__________________________________________________________________________________

    text = re.sub('(\w+)\++\s(\w+\.*\w*)', '\\1 \\2', text)
    text=re.sub('\(\(+', '(', text)
    text=re.sub('\)\)+', ')', text)
    text=re.sub('\%\)+', '', text)
    text=re.sub('/-l', '', text)
    text = re.sub('=', '', text)
    text=re.sub('% % /ál', '%', text)
    text=re.sub('% /ál', '%', text)
    text=re.sub('% /µl', '%', text)
    text=re.sub('\s+\-\s+', '-', text)
    text=re.sub('\s+\/\s+', '/', text)
    text=re.sub('\s\w+\.\w+\s\#\s\%\s\/.\w\s\(',' (',text)
    text=re.sub('\s\%(\s\w+\.\w+)\s\(','\\1 % (',text)
    text=re.sub('\s\%(\s\w+\.\w+)\s\w+\.+\w+\s\#\s\%', '\\1 %', text)
    text = re.sub('\s\%(\s\w+\.\w+)\s\w+\.+\w+\s\%\s\(', '\\1 % (', text)
    text=re.sub('% %', '%', text)


    #LIMPIAR TEXTO "text" de simbolos y apocrofes 11/06/2021
    try:
        text = text.replace('á', 'a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
        text = text.replace('à', 'a').replace('è','e').replace('ì','i').replace('ò','o').replace('ù','u')
        text = text.replace('*', '').replace('!', '').replace('¡', '').replace('?', '').replace('¿', '')
    except: print('\n\t\ttexto actualmente limpio'.upper())

    try:
        text = re.sub('hombres\s\w+\.*\w*\sa.+\n|mujeres\s\w+\.*\w*\sa.+\n', '', text)
        text = re.sub('mujeres\s<\s\w+.+\n|mujeres\s>\s\w+.+\n', '', text)
        text = re.sub('hombres\s<\s\w+.+\n|hombres\s>\s\w+.+\n', '', text)
    except:
        print('\n\tOK: No se encontro condicion para sustitucion')

    try:
        text = text.replace('seg ratio: ','seg_ratio:')
        text = text.replace('seg. ratio: ', 'seg_ratio:')
        text = text.replace('seg/ ratio: ', 'seg_ratio:')
        text = text.replace('seg /ratio: ', 'seg_ratio:')
        text = text.replace('seg /ratio: ', 'seg_ratio:')
        text = text.replace('ratio: ', 'seg_ratio:').replace('ratio:', 'seg_ratio:')
        text = text.replace('mm de hg', 'mm_de_hg')
        text = text.replace('+æ','ñ')
    except: print('\n\tOK: No se encontro condicion para sustitucion')

    try:
        text=text.replace('resultados validados\n','')
    except: print('\n\tOK: No se encontro condicion para sustitucion')

    try:
        text=text.replace('relaci¢n a/g','relacion ag')
    except: print('\n\tOK: No se encontro condicion para sustitucion')

    try:
        text=re.sub('\nmujeres\s\<(\w+)\s.+\nvarones\s\<(\w+).+',' (m 0-\\1 h 0-\\2)',text)
    except: print('\n\tOK: No se encontro condicion para sustitucion')

    try:
        text=re.sub('hombres\:.+\n','',text)
        text=re.sub('mujeres\:.+\n','',text)
    except: print('\n\tOK: No se encontro condicion para sustitucion')

    try:
        text=re.sub('\nhombres\s(\w+.\w+\-\w+\w+).+mujeres\s(\w+.\w+\-\w+\w+).+',' (m \\1 h \\2)',text)
    except: print('\n\tOK: No se encontro condicion para sustitucion')

    try:
        text=re.sub('(\d)\s(\w+\/\w+).+(\(.+\)\n)','\\1 \\2 \\3',text)
    except: print('\n\tOK: No se encontro condicion para sustitucion')

    try:                        #Agregado25/08/2021
        text = re.sub('\n(\w+\s\d+\.\d+)\n', '\n\\1 null (null)\n', text)
    except:
        print('\n\tOK: No se encontro condicion para sustitucion')

    try:
        text = re.sub(
            '\n(\w+\s*\,*\.*\w*\s*\,*\.*\w*\s*\,*\.*\w*\s*\,*\.*\w*\s*\,*\.*\w*\s*\,*\.*\w*\s*\,*\.*\w*\s\d+\.*\d*)\s*\n',
            '\n\\1 null (null)\n', text)
    except: print('\n\tOK: No se encontro condicion para sustitucion')

    try:
        text = re.sub(
            '\n(\w+\s*\,*\.*\-*\w*\s*\,*\.*\-*\w*\s*\,*\.*\-*\w*\s*\,*\.*\-*\w*\s*\,*\.*\-*\w*\s*\,*\.*\-*\w*\s*\,*\.*\-*\w*\s\-*\d+\.*\d*\s+\-*\w+\W*\w*)\s*\n',
            '\n\\1 (null)\n', text)
    except:
        print('\n\tOK: No se encontro condicion para sustitucion')

    try:
        text = re.sub(
            '\n(\w+\s*\,*\.*\-*\w*\s*\,*\.*\-*\w*\s*\,*\.*\-*\w*\s*\,*\.*\-*\w*\s*\,*\.*\-*\w*\s*\,*\.*\-*\w*\s*\,*\.*\-*\w*\s\-*\d+\.*\d*\s+\-*\w+\W*\w*)\s*\n',
            '\n\\1 (null)\n', text)
    except:
        print('\n\tOK: No se encontro condicion para sustitucion')

    try:
        text = re.sub(
            '\n(\w+\s*\,*\-*\/*\.*\w*\s*\,*\-*\/*\.*\w*\s*\,*\-*\/*\.*\w*\s*\,*\-*\/*\.*\w*\d)\s\(',
            '\n\\1 null (', text)
    except: print('\n\tOK: No se encontro condicion para sustitucion')

    try:
        text = re.sub('(\d\s\%)\n', '\\1 (null)\n', text)
    except:
        print('\n\tOK: No se encontro condicion para sustitucion')

    try:
        text=re.sub('valid.+\n','',text)
    except: print('\n\tOK: No se encontro condicion para sustitucion')

    try:
        text=re.sub('matr.cula:.+\n','',text)
    except: print('\n\tOK: No se encontro condicion para sustitucion')

    try:
        text=re.sub('c.dula:.+\n','',text)
    except: print('\n\tOK: No se encontro condicion para sustitucion')

    try:
        text=re.sub('fecha\sde\simpresi.n.+\n*','',text)
    except: print('\n\tOK: No se encontro condicion para sustitucion')

    try:
        text=re.sub('apartir\sdel\s.+\n*','',text)
    except: print('\n\tOK: No se encontro condicion para sustitucion')

    try:
        text=re.sub('aqui\semitidas\n*','',text)
    except: print('\n\tOK: No se encontro condicion para sustitucion')

    #Nueva Linea para quitar campo de Quimica-Clinica>General Orina
    try:
        textSplit=re.split('general de orina',text)
        text=textSplit[0]
        try:
            textSearch=re.search('inmunologia|quimica clinica|hematologia|inmuno-infecto|coagulaciones',textSplit[1])
            textSearch=textSearch.group(0)

            textSplit2=re.split('inmunologia|quimica clinica|hematologia|inmuno-infecto|coagulaciones',textSplit[1])
            text2=textSplit2[1]
            text=text+textSearch+text2
        except:print('\n\tNO se encontro estudios posteriores a quimica clinica')
    except: print('\n\tOK: No se encontro  \"general de orina\" para sustitucion')

    #Mensaje en estudio de inmunologia
    try:
        text=re.sub('deficiencia:.+\n','',text)
    except: print('\n\tOK: No se encontro condicion para sustitucion')
    try:
        text=re.sub('insuficiencia:.+\n','',text)
    except: print('\n\tOK: No se encontro condicion para sustitucion')
    try:
        text=re.sub('suficiencia:.+\n','',text)
    except: print('\n\tOK: No se encontro condicion para sustitucion')
    try:
        text=re.sub('toxicidad:.+\n','',text)
    except: print('\n\tOK: No se encontro condicion para sustitucion')
    try:
        text=re.sub('\(metodo utilizado:.+\n','',text)
    except: print('\n\tOK: No se encontro condicion para sustitucion')

    try:
        text=text.replace('>','').replace('<','')
    except: print('\n\tOK: No se encontro condicion para sustitucion')


    # Revision del texto extraido para pruebas ________________________________________
    f = open(str(rutaOrigen)+'\\TextFiles\\txtLaboratorio2.txt', 'w+')
    f.write(str(text))
    f.close()
    #__________________________________________________________________________________
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    #Obtencion de valores del TEXTO procesado***************************************************************************
    #valores Diccionario General_________________________________________________________
    # NSS
    try:
        nss = re.search(formatoNSS, text)
        nss = nss.group(1)
        nss = nss.replace(' ', '')
        if nss==dictGeneral['nss']:
            #conversion de string a double
            nss=int(nss)
            dictGeneral['nss']=nss
        else:
            errorExtracionNSS = str(dictGeneral['nss'])
    except:
        errorExtracionNSS=str(dictGeneral['nss'])

    # FOLIO DE LA ORDEN
    try:
        folioOrden = re.search(formatoFolioOrden, text)
        folioOrden = folioOrden.group(1)
        # conversion de string a double
        folioOrden=int(folioOrden)
        dictGeneral['folio_orden'] = folioOrden
    except:
        errorExtracionNSS=str(dictGeneral['nss'])

    # FECHA DE LA ORDEN
    try:
        fechaOrden = re.search(formatoFechaOrden, text)
        fechaOrden = fechaOrden.group(1)
        #Conversion a formato YYYY-MM-DD
        fechaOrden= datetime.datetime.strptime(fechaOrden, '%d/%m/%Y')
        dictGeneral['fecha_orden'] = fechaOrden
        #CAMBIAR FORMATO AAAA-MM-DD
    except:
        print('\tNo se cumplio condicion de busqueda: FECHA ORDEN')

    # EDAD
    try:
        edad = re.search(formatoEdad, text)
        edad = edad.group(1)
        edad=int(edad)
        dictGeneral['edad'] = edad
    except:
        print('\tNo se cumplio condicion de busqueda: EDAD')

    # SERVICIO SOLICITA
    try:
        servicio = re.search(formatoServicioSolicita, text)
        servicio = servicio.group(1)
        servicio = servicio.replace('…', '')
        servicio = re.sub('\d*\s*(\D+)', '\\1', servicio)
        dictGeneral['servicio_solicita'] = servicio
    except:
        print('\tNo se cumplio condicion de busqueda: SERVICIO SOLICITA')

    #Valores Estudios y Resultados_________________________________________________________
    textSplit=''

    try:
        textSplit = re.split('determinacion resultados unidades valores normales', text)
        for i in range(len(textSplit) - 1):
            reSearch = re.search('.+\n$', str(textSplit[i]))
            reSearch = reSearch.group()
            reSearch = reSearch.replace('\n', '')
            listEstudiosLabs.append(reSearch)
    except:
        print('\tNo se cumplio condicion de busqueda: SPLIT TEXTO|BUSQUEDA DE ESTUDIOS HECHOS')
        errorExtracionNSS=str(dictGeneral['nss'])

    if errorExtracionNSS=='':
        j = 0
        for i in range(1, len(textSplit)):
            listDeterminacion = []
            listResultados = []
            listUnidades = []
            listValoresNormales = []

            stringSustitutoDeterminacion = str(textSplit[i]).replace('\n', '@')

            # Valores de determinacion
            try:
                textFindall = re.findall(str(formatoDeterminacion), stringSustitutoDeterminacion)
                for k in range(len(textFindall)):
                    newText = str(textFindall[k])
                    newText = re.sub('\@(\w+\W*\w*\W*\w*\W*\w*\W*\w*\d*)\s\-*\d', '\\1', newText)
                    newText = re.sub('(\w+\W*\w*\W*\w*\W*\w*\W*\w*)\s*\%', '\\1', newText)
                    newText = re.sub('(\w+\W*\w*\W*\w*\W*\w*\W*\w*)\s*\:', '\\1', newText)
                    newText = re.sub('(\w+\W*\w*\W*\w*\W*\w*\W*\w*)\s*', '\\1', newText)
                    newText = newText.replace('@', '').replace(':', '')
                    listDeterminacion.append(str(newText))
                dictValoresEstudios['determinacion'] = listDeterminacion
            except:
                print('\t\tNo se cumplio condicion de busqueda: DETERMINACION')

            # Valores de resultado
            try:
                textFindall = re.findall(str(formatoResultados), str(textSplit[i]))
                for k in range(len(textFindall)):
                    newText = str(textFindall[k])
                    newText = re.sub('\s(.+)\s', '\\1', newText)
                    listResultados.append(newText)
                dictValoresEstudios['resultados'] = listResultados
            except:
                print('\t\tNo se cumplio condicion de busqueda: RESULTADOS')

            # Valores de unidades
            try:
                textFindall = re.findall(str(formatoUnidades), str(textSplit[i]))
                for k in range(len(textFindall)):
                    newText = str(textFindall[k])
                    newText = newText.replace('(', '')
                    newText = re.sub('\d\s(.+)\s', '\\1', newText)
                    newText = re.sub('(.+)\s*/al', '\\1', newText)
                    newText = re.sub('(.+)\s', '\\1', newText)
                    listUnidades.append(newText)
                dictValoresEstudios['unidades'] = listUnidades
            except:
                print('\t\tNo se cumplio condicion de busqueda: UNIDADES')

            # Valores de valore normales
            try:
                textFindall = re.findall(str(formatoValoresNormales), str(textSplit[i]))
                for k in range(len(textFindall)):
                    newText = str(textFindall[k])
                    newText = newText.replace(' (', '').replace(')', '')
                    listValoresNormales.append(newText)
                dictValoresEstudios['valores_normales'] = listValoresNormales
            except:
                print('\t\tNo se cumplio condicion de busqueda: UNIDADES')

            #print('\t\titerador para estudiosLabs: ', j)
            #print('\t\t',listEstudiosLabs[j])
            dictEstudios[str(listEstudiosLabs[j])] = dictValoresEstudios.copy()

            if len(listDeterminacion)==len(listResultados)  and \
                    len(listDeterminacion)==len(listUnidades) and \
                    len(listDeterminacion)==len(listValoresNormales):

                if len(listDeterminacion)>0 and len(listUnidades)>0 and len(listResultados)>0 and len(listValoresNormales)>0:
                    dictEstudios[str(listEstudiosLabs[j])] = dictValoresEstudios.copy()
                else:
                    dictEstudios.pop(str(listEstudiosLabs[j]))

            else:
                dictEstudios.pop(str(listEstudiosLabs[j]))

            j += 1

        dictGeneral['estudios']=dictEstudios.copy()


    #*******************************************************************************************************************

    #PENDIENTE: ERROR POR COMPARATIVA DE TAMAÑO DE LISTAS PARA CADA ESTUDIO

    resultado.append(dictGeneral)
    resultado.append(errorExtracionNSS)
    return resultado

def extraccionPDFNotaFinal(rutaPDF,diccEstandar):
    resultado=[]
    pagesText=""
    text=""
    textSplit=[]
    errorDate=False

    textPage=[]

    rutaActual = os.path.abspath(os.getcwd())

    errorExtracionNSS=''

    # Lectura y obtencion de texto de PDFs con pdfminer   ***************************
    output_string = StringIO()
    with open(str(rutaPDF), 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    text=output_string.getvalue()
    text=text.lower()

    # Revision del texto extraido para pruebas ________________________________________
    f = open(str(rutaActual)+'\\TextFiles\\pdfFinalMiner0.txt', 'w+')
    f.write(str(text))
    f.close()
    #__________________________________________________________________________________
    text = text.replace('\n ', ' ')
    text = text.replace('\n\n\n', '\n').replace('\n\n', '\n')
    text = text.replace('   ', ' ').replace('  ', ' ')

    try:
        textSplit=re.split('\n\x0c',text)
    except:
        print('\n\tNo hay paginas para separar'.upper())

    if len(textSplit)>1:
        text=str(textSplit[0])
        # QUITAR ENCABEZADOS
        for numPagina in range(1,len(textSplit)):
            textoSinEncabezado = None
            try:
                textoSinEncabezado = re.sub('instituto mexicano.+\n(.+\n)+\d+\/\d+\/\d+\s\-\s\d+\:\d+\n*', '', str(textSplit[numPagina]))
                text = str(text) + str(textoSinEncabezado)
            except: None
    textSplit=[]

    # Revision del texto extraido para pruebas ________________________________________
    f = open(str(rutaActual) + '\\TextFiles\\pdfFinalMiner1.txt', 'w+')
    f.write(str(text))
    f.close()
    # __________________________________________________________________________________
    try:
        text = text.replace('\x0c', '')
    except:None

    try:
        text = re.sub('\(cid:13\)', '',str(text))
    except:None

    try:
        text = re.sub('  ', ' ', str(text))
        text = re.sub('\n ', '\n',str(text))
        text = re.sub('\n\n+', '\n',str(text))
    except:None

    try:
        text = re.sub('\n \n', '\n',str(text))
    except:None

    # Revision del texto extraido para pruebas ________________________________________
    f = open(str(rutaActual)+'\\TextFiles\\pdfFinalMiner2.txt', 'w+')
    f.write(str(text))
    f.close()
    #__________________________________________________________________________________

    #LIMPIAR TEXTO "text" de simbolos y apocrofes 11/06/2021
    try:
        text = text.replace('á', 'a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
        text = text.replace('à', 'a').replace('è','e').replace('ì','i').replace('ò','o').replace('ù','u')
        text = text.replace('*', '').replace('!', '').replace('¡', '').replace('?', '').replace('¿', '')
    except:
        print('\n\t\ttexto actualmente limpio'.upper())

    # Revision del texto extraido para pruebas ________________________________________
    f = open(str(rutaActual)+'\\TextFiles\\pdfFinalMiner3.txt', 'w+')
    f.write(str(text))
    f.close()
    #__________________________________________________________________________________

    listaBusquedaNotaInicial = soportFuntions.estructuraNotaFinal()

    listTextoBuscado=listaBusquedaNotaInicial[0]
    listaTextoDelimitador=listaBusquedaNotaInicial[1]
    listFormatoBuscado=listaBusquedaNotaInicial[2]
    listaValorDiccionario=listaBusquedaNotaInicial[3]

    #dividir texto string en partes para extraccion del contenido

    if len(listTextoBuscado) == len(listFormatoBuscado):
        sizeList = len(listTextoBuscado)

    for iterador in range(sizeList):
        TextSplit = []
        TextSplit = re.split(str(listTextoBuscado[iterador]), str(text), 2)

        #AGREGAR ACONDCIONAMIENTO DE TEXTO text=text.replace('\n', '')
        for numSplit in range(len(TextSplit)):
            TextSplit[numSplit] = TextSplit[numSplit].replace('\n', ' ')
            TextSplit[numSplit] = TextSplit[numSplit].replace('   ', ' ').replace('  ', ' ')

        if len(TextSplit) > 1:
            reSearch = re.findall(str(listFormatoBuscado[iterador]), str(TextSplit[1]))

            if not reSearch:
                reSearch = None
            elif listaTextoDelimitador[iterador] != '':
                reSearch = re.split(str(listaTextoDelimitador[iterador]), str(reSearch[0]), 2)
                reSearch = reSearch[0]
            else:
                reSearch = reSearch[0]
        else:
            reSearch = None

        #agregar eliminacion de espacio al final del string
        if reSearch:
            reSearch=re.sub('^\s*', '', reSearch)
            reSearch = re.sub('$\s*', '', reSearch)

        if reSearch: print('Valor encontrado: '.upper() + reSearch)
        else: print('Valor encontrado: '.upper() + "NULL")

        #DETECTAR SI TEXTO ES FECHA
        # Try Catch por falla de lectura en apartado "fecha de clasificacion"
        try:
            if listTextoBuscado[iterador]=="Fecha de Clasificacion:".lower():
                #Conversion a formato YYYY-MM-DD
                reSearch= datetime.datetime.strptime(reSearch, '%d/%m/%Y')
            elif listTextoBuscado[iterador]=="\\nFECHA DE INGRESO".lower():
                #Conversion a formato YYYY-MM-DD
                reSearch= datetime.datetime.strptime(reSearch, '%d/%m/%Y')
            else:None

        except:
            errorDate=True

        #CASO PARA CUANDO reSearch pueda convertirse de str a decimal
        try:
            reSearch=float(reSearch)
        except:
            pass

        # Agregar valor reSearch a diccionario
        diccEstandar[str(listaValorDiccionario[iterador])] = reSearch

        #Try Catch por falla de lectura en apartado "Resumen del Interrogatorio"
        if ((str(listTextoBuscado[iterador]))=="RESUMEN DE EVOLUCION".lower()) and (reSearch==None):
            errorExtracionNSS=(str(diccEstandar['nss']))

        elif errorDate:
            errorExtracionNSS=(str(diccEstandar['nss']))

    resultado.append(diccEstandar.copy())
    resultado.append(errorExtracionNSS)

    return resultado
#---------------------------------------------------------------------

def pdfsPendientes(ruta):
    resultado=[]

    NumeroTotalDePDFs=0
    PDFsListaDeNombresActuales = []
    PDFsListaDeRutasCompletas=[]

    contenido = os.listdir(ruta)

    #Evaluacion del numero total de PDFs en la ruta y sus nombres
    for fichero in contenido:
        if os.path.isfile(os.path.join(ruta, fichero)) and fichero.endswith('.pdf'):
            PDFsListaDeNombresActuales.append(fichero)
    NumeroTotalDePDFs=len(PDFsListaDeNombresActuales)

    if NumeroTotalDePDFs>0:
        for number in range(NumeroTotalDePDFs):
            PDFsListaDeRutasCompletas.append(str(ruta)+'\\'+str(PDFsListaDeNombresActuales[number]))

    resultado=[NumeroTotalDePDFs,PDFsListaDeRutasCompletas]

    return resultado

def pdfsOrganizar(rutaOrigen,rutasNotaClase,rutasNotasClaseDX,rutaPDF):
    resultado=None

    tituloPDF=None
    FolioLabPDF=None
    typePDF=None
    foundN=False
    foundE=False
    foundC=False
    pagesText=""
    text=""
    fileDestiny=None
    DxFinal=None
    newPDFname = None
    PDFrep=0

    # Lectura y obtencion de texto de PDFs con pdfminer   ***************************
    output_string = StringIO()
    with open(str(rutaPDF), 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    text=output_string.getvalue()
    text=text.lower()
    #***************************************************************************************

    # Deteccion del tipo de PDF
    try:
        if tituloPDF == None:
            tituloPDF = re.search("nota inicial urgencias|nota de ingreso", text)
            tituloPDF = str(tituloPDF.group())
            typePDF = 1
    except:
        pass
    try:
        if tituloPDF == None:
            tituloPDF = re.search("nota interconsulta", text)
            tituloPDF = str(tituloPDF.group())
            typePDF = 2
    except:
        pass
    try:
        if tituloPDF == None:
            tituloPDF = re.search("nota de egreso|nota de pre-alta", text)
            tituloPDF = str(tituloPDF.group())
            typePDF = 3
    except:
        pass
    try:
        if tituloPDF == None:
            tituloPDF = re.search("hoja de resultados", text)
            tituloPDF = str(tituloPDF.group())
                    #AGREGAR FOLIO_ORDEN AL NOMBRE DEL ARCHIVO
            FolioLabPDF=re.search("folio de la orden:\s*(\d+)", text)
            FolioLabPDF=str(FolioLabPDF.group(1))
            typePDF = 4
    except:
        typePDF = 5 #Otro tipo

    # NOTA INICIAL URGENCIAS=
    if typePDF==1:
        #Obtencion del NSS
        NSS = re.findall(r"nss\:(\s*\d+\s*\d*\s*\d*\s*\d*\s*\d*)", str(text))
        NSS = str(NSS[0])
        NSS = NSS.replace(" ", "")

        newPDFname=str(NSS)+"_NotaInicial.pdf"
        rutaNuevaPDF = str(rutasNotaClase[1]) + '\\' + str(newPDFname)

        try:
            if not os.path.exists(str(rutaNuevaPDF)): os.rename(str(rutaPDF), str(rutaNuevaPDF))
            else: os.rename(str(rutaPDF), str(rutasNotaClase[5]) + '\\Existente_'+ str(newPDFname))
        except:
            PDFrep+=1
            os.rename(str(rutaPDF), str(rutasNotaClase[5]) + '\\Existente' + str(PDFrep)+'_'+str(newPDFname))

    # NOTA INTERCONSULTA
    if typePDF==2:
        #Obtencion del NSS
        NSS = re.findall(r"nss\:(\s*\d+\s*\d*\s*\d*\s*\d*\s*\d*)", str(text))
        NSS = str(NSS[0])
        NSS = NSS.replace(" ", "")

        newPDFname=str(NSS)+"_NotaInterconsulta.pdf"
        rutaNuevaPDF = str(rutasNotaClase[2]) + '\\' + str(newPDFname)

        try:
            if not os.path.exists(str(rutaNuevaPDF)):
                os.rename(str(rutaPDF), str(rutaNuevaPDF))
            else:
                os.rename(str(rutaPDF), str(rutasNotaClase[5]) + '\\Existente_' + str(newPDFname))
        except:
            PDFrep += 1
            os.rename(str(rutaPDF), str(rutasNotaClase[5]) + '\\Existente' + str(PDFrep) + '_' + str(newPDFname))

    #NOTA FINAL DE EGRESO
    if typePDF == 3:
        # Obtencion del NSS
        NSS = re.findall(r"nss\:(\s*\d+\s*\d*\s*\d*\s*\d*\s*\d*)", str(text))
        NSS = str(NSS[0])
        NSS = NSS.replace(" ", "")

        # Separacion del Texto completo
        TxtSplit = re.split(r'diagnosticos\s\bde\s\begreso|resumen\s\bde\s\bevolucion', text)

        # Deteccion de codigos de "EGRESO"
        SearchCodeEgreso = re.findall(r"[a-zA-Z]\d\d\w", str(TxtSplit[1]))

        # llamar lista de codigos formato txt
        CodigosCIE = soportFuntions.codesCIE10(rutaOrigen)
        CodeNeumonia = CodigosCIE[0]
        CodeEmbolia = CodigosCIE[1]
        CodeControl = CodigosCIE[2]             #Añadido Control 29/04/2021

        for i in SearchCodeEgreso:
            for j in CodeNeumonia:
                if j == i:
                    foundN = True
                    break

        for i in SearchCodeEgreso:
            for j in CodeEmbolia:
                if j == i:
                    foundE = True
                    break

        #Añadido Control 29/04/2021------------------
        for i in SearchCodeEgreso:
            for j in CodeControl:
                if j == i:
                    foundC = True
                    break

        # Añadido Control 29/04/2021-------------------
        if foundC:
            DxFinal = "Control"

            newPDFname = str(NSS)+"_NotaFinal_"+str(DxFinal)+".pdf"
            rutaNuevaPDF = str(rutasNotasClaseDX[2]) + '\\' + str(newPDFname)
            try:
                if not os.path.exists(str(rutaNuevaPDF)):
                    os.rename(str(rutaPDF), str(rutaNuevaPDF))
                else:
                    os.rename(str(rutaPDF), str(rutasNotaClase[5]) + '\\Existente_' + str(newPDFname))
            except:
                PDFrep += 1
                os.rename(str(rutaPDF), str(rutasNotaClase[5]) + '\\Existente' + str(PDFrep) + '_' + str(newPDFname))
        #--------------------------------------------


        elif foundN and foundE:
            DxFinal = "Ambos"

            newPDFname = str(NSS)+"_NotaFinal_"+str(DxFinal)+".pdf"
            rutaNuevaPDF = str(rutasNotasClaseDX[3]) + '\\' + str(newPDFname)
            try:
                if not os.path.exists(str(rutaNuevaPDF)):
                    os.rename(str(rutaPDF), str(rutaNuevaPDF))
                else:
                    os.rename(str(rutaPDF), str(rutasNotaClase[5]) + '\\Existente_' + str(newPDFname))
            except:
                PDFrep += 1
                os.rename(str(rutaPDF), str(rutasNotaClase[5]) + '\\Existente' + str(PDFrep) + '_' + str(newPDFname))

        elif foundN:
            DxFinal = "Neumonia"

            newPDFname = str(NSS)+"_NotaFinal_"+str(DxFinal)+".pdf"
            rutaNuevaPDF = str(rutasNotasClaseDX[0]) + '\\' + str(newPDFname)
            try:
                if not os.path.exists(str(rutaNuevaPDF)):
                    os.rename(str(rutaPDF), str(rutaNuevaPDF))
                else:
                    os.rename(str(rutaPDF), str(rutasNotaClase[5]) + '\\Existente_' + str(newPDFname))
            except:
                PDFrep += 1
                os.rename(str(rutaPDF), str(rutasNotaClase[5]) + '\\Existente' + str(PDFrep) + '_' + str(newPDFname))

        elif foundE:
            DxFinal = "Embolia"

            newPDFname = str(NSS)+"_NotaFinal_"+str(DxFinal)+".pdf"
            rutaNuevaPDF = str(rutasNotasClaseDX[1]) + '\\' + str(newPDFname)
            try:
                if not os.path.exists(str(rutaNuevaPDF)):
                    os.rename(str(rutaPDF), str(rutaNuevaPDF))
                else:
                    os.rename(str(rutaPDF), str(rutasNotaClase[5]) + '\\Existente_' + str(newPDFname))
            except:
                PDFrep += 1
                os.rename(str(rutaPDF), str(rutasNotaClase[5]) + '\\Existente' + str(PDFrep) + '_' + str(newPDFname))

        else:
            DxFinal = "Otros"

            newPDFname = str(NSS)+"_NotaFinal_"+str(DxFinal)+".pdf"
            rutaNuevaPDF = str(rutasNotasClaseDX[3]) + '\\' + str(newPDFname)
            try:
                if not os.path.exists(str(rutaNuevaPDF)):
                    os.rename(str(rutaPDF), str(rutaNuevaPDF))
                else:
                    os.rename(str(rutaPDF), str(rutasNotaClase[5]) + '\\Existente_' + str(newPDFname))
            except:
                PDFrep += 1
                os.rename(str(rutaPDF), str(rutasNotaClase[5]) + '\\Existente' + str(PDFrep) + '_' + str(newPDFname))

    #RESULTADOS DE LABORATORIO
    if typePDF==4:
        #Obtencion del NSS
        NSS = re.findall(r"\d\d\d\d\s\d\d\s\d\d\d\d", str(text))
        NSS = str(NSS[0])
        NSS = NSS.replace(" ", "")

        newPDFname=str(NSS)+"-"+str(FolioLabPDF)+"_HojaLab.pdf"
        rutaNuevaPDF = str(rutasNotaClase[4]) + '\\' + str(newPDFname)

        try:
            if not os.path.exists(str(rutaNuevaPDF)):
                os.rename(str(rutaPDF), str(rutaNuevaPDF))
            else:
                os.rename(str(rutaPDF), str(rutasNotaClase[5]) + '\\Existente_' + str(newPDFname))
        except:
            PDFrep += 1
            os.rename(str(rutaPDF), str(rutasNotaClase[5]) + '\\Existente' + str(PDFrep) + '_' + str(newPDFname))

    return resultado

#Evaluacion de carpetas y creacion de diccionarios
def pdfsNotaInicial(rutaOrigen,rutaCarpetaPDFs,rutaCarpetaErrorPDFS,archivos_en_BD):
    resultado=[]
    PDFsListNSSActuales=[]

    PDFsListNSSFloat=[]
    indexListNSS=[]

    diccGeneralPacientes={}
    diccGeneralNotaInicial={}

    listaErroresNSS=[]
    # Consultar registro de notas iniciales en Base de Datos *********************************************************
    if len(archivos_en_BD)>0:
        contenidoCarpeta = os.listdir(rutaCarpetaPDFs)
        for fichero in contenidoCarpeta:
            notaInicialNSS = re.search("\d*", str(fichero))
            notaInicialNSS = notaInicialNSS.group()
            PDFsListNSSActuales.append(notaInicialNSS)

        for valorFolio in PDFsListNSSActuales:
            valorFloat=None
            try:
                valorFloat=float(valorFolio)
                PDFsListNSSFloat.append(valorFloat)
            except: print('\tError con conversion a float'.upper())

        for valor in PDFsListNSSFloat:
            index=None
            if valor in archivos_en_BD:
                index=PDFsListNSSFloat.index(valor)
                indexListNSS.append(index)

        for index in sorted(indexListNSS, reverse=True):
            del contenidoCarpeta[index]

    else:
        contenidoCarpeta = os.listdir(rutaCarpetaPDFs)

    #________________________________________________________________________________________________________________
    if len(contenidoCarpeta)>0:
        PDFsListNSSActuales.clear()

        for fichero in contenidoCarpeta:
            if os.path.isfile(os.path.join(rutaCarpetaPDFs, fichero)) and fichero.endswith('.pdf'):
                notaInicialNSS = re.search("\d*", str(fichero))
                notaInicialNSS = notaInicialNSS.group()
                PDFsListNSSActuales.append(notaInicialNSS)
                rutaFilePDF=str(rutaCarpetaPDFs)+'\\'+str(fichero)


                diccEstandarNotaInicial=soportFuntions.setDictNotaInicial()
                    #agregacion del NSS a diccionario
                diccEstandarNotaInicial['nss'] = str(notaInicialNSS)


                resPDFNotaInicial=extraccionPDFNotaInicial(rutaFilePDF,diccEstandarNotaInicial)

                #Revision de error con lectura del PDF:
                if resPDFNotaInicial[1]!='':
                    listaErroresNSS.append(resPDFNotaInicial[1])
                    os.rename(str(rutaFilePDF), str(rutaCarpetaErrorPDFS) + '\\FAIL-' + str(fichero))


                datosNotaInicial=resPDFNotaInicial[0]
                diccGeneralNotaInicial[str(notaInicialNSS)]=datosNotaInicial.copy()
        #FIN FOR

        llavesNotaInicial=diccGeneralNotaInicial.keys()
        llavesNotaInicial=list(llavesNotaInicial)

        for key in llavesNotaInicial:
            diccGeneralPacientes.update({key:{'nss':key}})


        if listaErroresNSS:
            #Impresion de errores detectados:
            rutaActual = os.path.abspath(os.getcwd())
            f = open(str(rutaActual) + '\\TextFiles\\DiccErroresNSS.txt', 'w')
            f.write(str(listaErroresNSS))
            f.close()

            # Eliminacion de KEYS con errores detectados:
            for i in listaErroresNSS:
                del diccGeneralPacientes[str(i)]
                del diccGeneralNotaInicial[str(i)]
                #MOVER ARCHIVOS CON ERROR A OTRA CARPETA
    else:
        print('\n\t\tNO HAY NUEVOS ARCHIVOS A EVALUAR...:D !!!'.upper())

    resultado.append(diccGeneralPacientes.copy())
    resultado.append(diccGeneralNotaInicial.copy())
    return resultado

def pdfsLaboratorio(rutaOrigen,rutaCarpetaPDFs,rutaCarpetaErrorPDFS,archivos_en_BD):
    resultado = {}
    PDFsListNSSActuales = []
    PDFsListFOLIOSActuales=[]

    PDFsListFOLIOSFloat=[]
    indexListFolios=[]

    listaBusquedaLaboratorio=[]
    listaErroresNSS = []

    diccGeneralLaboratorio = {}
    diccFolioLaboratorio={}
    diccEstandarLaboratorio={}

    NSS = None
    FOLIO = None
    reSearch = None
    resPDFNLaboratorio = None
    datosLaboratorio = None
    resPDFNLaboratorio = None


    # Consultar registro de notas iniciales en Base de Datos *********************************************************
    if len(archivos_en_BD)>0:

        contenidoCarpeta = os.listdir(rutaCarpetaPDFs)
        for fichero in contenidoCarpeta:
            reSearch = re.search("\d+-(\d+)", str(fichero))
            FOLIO = reSearch.group(1)
            PDFsListFOLIOSActuales.append(FOLIO)

        for valorFolio in PDFsListFOLIOSActuales:
            valorFloat=None
            try:
                valorFloat=float(valorFolio)
                PDFsListFOLIOSFloat.append(valorFloat)
            except: print('\tError con conversion a float'.upper())

        for valor in PDFsListFOLIOSFloat:
            index=None
            if valor in archivos_en_BD:
                index=PDFsListFOLIOSFloat.index(valor)
                indexListFolios.append(index)
            else:
                print('\n\tValor: '.upper(),valor,' no existente en base de datos'.upper())

        for index in sorted(indexListFolios, reverse=True):
            del contenidoCarpeta[index]

    else:
        contenidoCarpeta = os.listdir(rutaCarpetaPDFs)


    # ________________________________________________________________________________________________________________
    if len(contenidoCarpeta)>0:
        PDFsListFOLIOSFloat.clear()
        PDFsListFOLIOSActuales.clear()

        for fichero in contenidoCarpeta:
            if os.path.isfile(os.path.join(rutaCarpetaPDFs, fichero)) and fichero.endswith('.pdf'):
                reSearch = re.search("(\d+)-(\d+)", str(fichero))
                NSS = reSearch.group(1)
                FOLIO=reSearch.group(2)
                PDFsListFOLIOSActuales.append(FOLIO)

                # Comparar NSS ACTUAL VS ANTERIOR
                if PDFsListNSSActuales:
                    if not NSS in PDFsListNSSActuales:
                        PDFsListNSSActuales.append(NSS)
                        diccFolioLaboratorio.clear()
                else:
                    PDFsListNSSActuales.append(NSS)

                rutaFilePDF=str(rutaCarpetaPDFs)+'\\'+str(fichero)

                listaFormatosLaboratorio = soportFuntions.estructuraLaboratorio()
                listDiccionario=soportFuntions.setDictLaboratorio()
                diccEstandarLaboratorio=listDiccionario[0]
                    #agregacion del NSS a diccionario
                diccEstandarLaboratorio['nss'] = str(NSS)

                resPDFNLaboratorio=extraccionPDFLaboratorio(rutaFilePDF,listaFormatosLaboratorio,listDiccionario)

                #Revision de error con lectura del PDF:
                if resPDFNLaboratorio[1]!='':
                    listaErroresNSS.append(resPDFNLaboratorio[1])
                    os.rename(str(rutaFilePDF), str(rutaCarpetaErrorPDFS) + '\\FAIL-' + str(fichero))
                else: None

                datosLaboratorio=resPDFNLaboratorio[0]
                diccFolioLaboratorio[str(FOLIO)]=datosLaboratorio.copy()
                #diccFolioLaboratorio.update({str(FOLIO): datosLaboratorio})

                diccGeneralLaboratorio[str(NSS)]=diccFolioLaboratorio.copy()
                #diccGeneralLaboratorio.update({str(NSS): diccFolioLaboratorio})

                resPDFNLaboratorio.clear()
                datosLaboratorio.clear()
            else:None
        #Fin For

        if listaErroresNSS:
            #Impresion de errores detectados:
            rutaActual = os.path.abspath(os.getcwd())
            f = open(str(rutaActual) + '\\TextFiles\\DiccErroresNSS.txt', 'w')
            f.write(str(listaErroresNSS))
            f.close()

            # Eliminacion de KEYS con errores detectados:
            for i in listaErroresNSS:
                del diccGeneralLaboratorio[str(i)]
            #Fin For
        else:None

    else:
        print('\n\t\tNO HAY NUEVOS ARCHIVOS A EVALUAR...:D !!!'.upper())

    resultado = diccGeneralLaboratorio.copy()
    return resultado

def pdfsNotaEgreso(rutaOrigen,rutaCarpetaPDFs,rutaCarpetaErrorPDFS,archivos_en_BD):
    resultado={}
    PDFsListNSSActuales=[]
    PDFsListNSSFloat=[]
    indexListNSS=[]
    listaErroresNSS=[]
    contenidoCarpeta=[]
    contenidoCarpetaEgreso=[]

    diccGeneralNotaFinal={}

    rutaCarpetaNeumonia=''
    rutaCarpetaEmbolia=''
    rutaCarpetaControl=''

    #Desgrose de rutas de egreso
    contenidoCarpeta = os.listdir(rutaCarpetaPDFs)
    rutaCarpetaNeumonia=str(rutaCarpetaPDFs)+'\\'+str(contenidoCarpeta[0])
    rutaCarpetaEmbolia=str(rutaCarpetaPDFs)+'\\'+str(contenidoCarpeta[1])
    rutaCarpetaControl=str(rutaCarpetaPDFs)+'\\'+str(contenidoCarpeta[2])

    contenidoCarpeta=[]

    # Consultar registro de notas finales en Base de Datos *********************************************************
    if len(archivos_en_BD)>0:
        PDFsListNSSActuales=[[],[],[]]
        PDFsListNSSFloat=[[],[],[]]
        indexListNSS=[[],[],[]]
        #Carpeta 1-Neumonia____________________________________
        contenidoCarpeta = []
        contenidoCarpeta=os.listdir(rutaCarpetaNeumonia)
        for fichero in contenidoCarpeta:
            notaFinalNSS = re.search("\d*", str(fichero))
            notaFinalNSS = notaFinalNSS.group()
            PDFsListNSSActuales[0].append(notaFinalNSS)
        notaFinalNSS=None
        contenidoCarpetaEgreso.append(contenidoCarpeta.copy())

        #Carpeta 2-Embolia____________________________________
        contenidoCarpeta = []
        contenidoCarpeta=os.listdir(rutaCarpetaEmbolia)
        for fichero in contenidoCarpeta:
            notaFinalNSS = re.search("\d*", str(fichero))
            notaFinalNSS = notaFinalNSS.group()
            PDFsListNSSActuales[1].append(notaFinalNSS)
        notaFinalNSS=None
        contenidoCarpetaEgreso.append(contenidoCarpeta.copy())

        #Carpeta 3-Control____________________________________
        contenidoCarpeta = []
        contenidoCarpeta=os.listdir(rutaCarpetaControl)
        for fichero in contenidoCarpeta:
            notaFinalNSS = re.search("\d*", str(fichero))
            notaFinalNSS = notaFinalNSS.group()
            PDFsListNSSActuales[2].append(notaFinalNSS)
        notaFinalNSS=None
        contenidoCarpetaEgreso.append(contenidoCarpeta.copy())

        #Conversion de valor String a Flotante (almacenado en BD)
        #Neumonia
        for valorNSS in PDFsListNSSActuales[0]:
            valorFloat=None
            try:
                valorFloat=float(valorNSS)
                PDFsListNSSFloat[0].append(valorFloat)
            except: print('\tError con conversion a float'.upper())

        #Embolia
        for valorNSS in PDFsListNSSActuales[1]:
            valorFloat=None
            try:
                valorFloat=float(valorNSS)
                PDFsListNSSFloat[1].append(valorFloat)
            except: print('\tError con conversion a float'.upper())

        #Control
        for valorNSS in PDFsListNSSActuales[2]:
            valorFloat=None
            try:
                valorFloat=float(valorNSS)
                PDFsListNSSFloat[2].append(valorFloat)
            except: print('\tError con conversion a float'.upper())

        #Comparativa entre valores KEY (flotante) de Carpetas vs Base de Datos
        #Neumonia
        for valor in PDFsListNSSFloat[0]:
            index=None
            if valor in archivos_en_BD:
                index=PDFsListNSSFloat[0].index(valor)
                indexListNSS[0].append(index)

        #Embolia
        for valor in PDFsListNSSFloat[1]:
            index=None
            if valor in archivos_en_BD:
                index=PDFsListNSSFloat[1].index(valor)
                indexListNSS[1].append(index)

        #Control
        for valor in PDFsListNSSFloat[2]:
            index=None
            if valor in archivos_en_BD:
                index=PDFsListNSSFloat[2].index(valor)
                indexListNSS[2].append(index)

        #Eliminacion de KEY de carpeta existente en Base de Datos por Index de lista
        #Neumonia
        for index in sorted(indexListNSS[0], reverse=True):
            del contenidoCarpetaEgreso[0][index]

        #Embolia
        for index in sorted(indexListNSS[1], reverse=True):
            del contenidoCarpetaEgreso[1][index]

        #Control
        for index in sorted(indexListNSS[2], reverse=True):
            del contenidoCarpetaEgreso[2][index]

    else:
        contenidoCarpetaEgreso.append(os.listdir(rutaCarpetaNeumonia))
        contenidoCarpetaEgreso.append(os.listdir(rutaCarpetaEmbolia))
        contenidoCarpetaEgreso.append(os.listdir(rutaCarpetaControl))
    #________________________________________________________________________________________________________________
    if len(contenidoCarpetaEgreso[0])>0:
        PDFsListNSSActuales.clear()
        diccEstandarNotaFinal={}

        for fichero in contenidoCarpetaEgreso[0]:

            if os.path.isfile(os.path.join(rutaCarpetaNeumonia, fichero)) and fichero.endswith('.pdf'):
                notaFinalNSS = re.search("\d*", str(fichero))
                notaFinalNSS = notaFinalNSS.group()
                PDFsListNSSActuales.append(notaFinalNSS)
                rutaFilePDF=str(rutaCarpetaNeumonia)+'\\'+str(fichero)


                diccEstandarNotaFinal=soportFuntions.setDictNotaFinal()
                    #agregacion del NSS a diccionario
                diccEstandarNotaFinal['nss'] = str(notaFinalNSS)
                diccEstandarNotaFinal['diagnostico_final'] = 'neumonia'


                resPDFNotaFinal=extraccionPDFNotaFinal(rutaFilePDF,diccEstandarNotaFinal)

                #Revision de error con lectura del PDF:
                if resPDFNotaFinal[1]!='':
                    listaErroresNSS.append(resPDFNotaFinal[1])
                    os.rename(str(rutaFilePDF), str(rutaCarpetaErrorPDFS) + '\\FAIL-' + str(fichero))


                datosNotaFinal=resPDFNotaFinal[0]
                diccGeneralNotaFinal[str(notaFinalNSS)]=datosNotaFinal.copy()
        #FIN FOR

        llavesNotaFinal=diccGeneralNotaFinal.keys()
        llavesNotaFinal=list(llavesNotaFinal)

        if listaErroresNSS:
            #Impresion de errores detectados:
            rutaActual = os.path.abspath(os.getcwd())
            f = open(str(rutaActual) + '\\TextFiles\\DiccErroresNSSNeumonia.txt', 'w')
            f.write(str(listaErroresNSS))
            f.close()

            # Eliminacion de KEYS con errores detectados:
            for i in listaErroresNSS:
                del diccGeneralNotaFinal[str(i)]
                #MOVER ARCHIVOS CON ERROR A OTRA CARPETA
    else:
        print('\n\t\tNO HAY NUEVOS ARCHIVOS DE NEUMONIA A EVALUAR...:D !!!'.upper())

    if len(contenidoCarpetaEgreso[1])>0:
        PDFsListNSSActuales.clear()
        diccEstandarNotaFinal={}

        for fichero in contenidoCarpetaEgreso[1]:

            if os.path.isfile(os.path.join(rutaCarpetaEmbolia, fichero)) and fichero.endswith('.pdf'):
                notaFinalNSS = re.search("\d*", str(fichero))
                notaFinalNSS = notaFinalNSS.group()
                PDFsListNSSActuales.append(notaFinalNSS)
                rutaFilePDF=str(rutaCarpetaEmbolia)+'\\'+str(fichero)


                diccEstandarNotaFinal=soportFuntions.setDictNotaFinal()
                    #agregacion del NSS a diccionario
                diccEstandarNotaFinal['nss'] = str(notaFinalNSS)
                diccEstandarNotaFinal['diagnostico_final'] = 'embolia'


                resPDFNotaFinal=extraccionPDFNotaFinal(rutaFilePDF,diccEstandarNotaFinal)

                #Revision de error con lectura del PDF:
                if resPDFNotaFinal[1]!='':
                    listaErroresNSS.append(resPDFNotaFinal[1])
                    os.rename(str(rutaFilePDF), str(rutaCarpetaErrorPDFS) + '\\FAIL-' + str(fichero))


                datosNotaFinal=resPDFNotaFinal[0]
                diccGeneralNotaFinal[str(notaFinalNSS)]=datosNotaFinal.copy()
        #FIN FOR

        llavesNotaFinal=diccGeneralNotaFinal.keys()
        llavesNotaFinal=list(llavesNotaFinal)

        if listaErroresNSS:
            #Impresion de errores detectados:
            rutaActual = os.path.abspath(os.getcwd())
            f = open(str(rutaActual) + '\\TextFiles\\DiccErroresNSSEmbolia.txt', 'w')
            f.write(str(listaErroresNSS))
            f.close()

            # Eliminacion de KEYS con errores detectados:
            for i in listaErroresNSS:
                del diccGeneralNotaFinal[str(i)]
                #MOVER ARCHIVOS CON ERROR A OTRA CARPETA
    else:
        print('\n\t\tNO HAY NUEVOS ARCHIVOS DE EMBOLIA A EVALUAR...:D !!!'.upper())

    if len(contenidoCarpetaEgreso[2])>0:
        PDFsListNSSActuales.clear()
        diccEstandarNotaFinal={}

        for fichero in contenidoCarpetaEgreso[2]:

            if os.path.isfile(os.path.join(rutaCarpetaControl, fichero)) and fichero.endswith('.pdf'):
                notaFinalNSS = re.search("\d*", str(fichero))
                notaFinalNSS = notaFinalNSS.group()
                PDFsListNSSActuales.append(notaFinalNSS)
                rutaFilePDF=str(rutaCarpetaControl)+'\\'+str(fichero)


                diccEstandarNotaFinal=soportFuntions.setDictNotaFinal()
                    #agregacion del NSS a diccionario
                diccEstandarNotaFinal['nss'] = str(notaFinalNSS)
                diccEstandarNotaFinal['diagnostico_final'] = 'control'


                resPDFNotaFinal=extraccionPDFNotaFinal(rutaFilePDF,diccEstandarNotaFinal)

                #Revision de error con lectura del PDF:
                if resPDFNotaFinal[1]!='':
                    listaErroresNSS.append(resPDFNotaFinal[1])
                    os.rename(str(rutaFilePDF), str(rutaCarpetaErrorPDFS) + '\\FAIL-' + str(fichero))


                datosNotaFinal=resPDFNotaFinal[0]
                diccGeneralNotaFinal[str(notaFinalNSS)]=datosNotaFinal.copy()
        #FIN FOR

        llavesNotaFinal=diccGeneralNotaFinal.keys()
        llavesNotaFinal=list(llavesNotaFinal)

        if listaErroresNSS:
            #Impresion de errores detectados:
            rutaActual = os.path.abspath(os.getcwd())
            f = open(str(rutaActual) + '\\TextFiles\\DiccErroresNSSControl.txt', 'w')
            f.write(str(listaErroresNSS))
            f.close()

            # Eliminacion de KEYS con errores detectados:
            for i in listaErroresNSS:
                del diccGeneralNotaFinal[str(i)]
                #MOVER ARCHIVOS CON ERROR A OTRA CARPETA
    else:
        print('\n\t\tNO HAY NUEVOS ARCHIVOS DE CONTROL A EVALUAR...:D !!!'.upper())


    resultado=diccGeneralNotaFinal.copy()

    return resultado
