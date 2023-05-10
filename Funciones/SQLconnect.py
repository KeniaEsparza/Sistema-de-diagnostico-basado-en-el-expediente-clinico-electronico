import mysql.connector as sql

def closeDBconect(db_connection):
    db_connection.close()
    return None

def testMySQLconect(propiedadesUsuario):
    resultado=None
    DBconectOK=False
    BDexist=0
    db_connection = None        # Variable conector SQL con base de datos
    db_cursor=None              #Variaable cursor para interacturar con base de datos
    host_user = propiedadesUsuario[0]
    usuario = propiedadesUsuario[1]
    contra = propiedadesUsuario[2]
    dbName= propiedadesUsuario[3]

    # Establecer Conexion --------------------------------------------------------------------
    try:
        db_connection = sql.connect(
            host=host_user,
            user=usuario,
            passwd=contra,
        )

        db_cursor = db_connection.cursor()
        db_cursor.execute("SHOW DATABASES")

        for db in db_cursor:
            if dbName in db[0]:
                BDexist = 1
                break

        if BDexist == 1:
            DBconectOK=True
        else:
            print("\tBase de datos: " + str(dbName) + ", NO existente")

        closeDBconect(db_connection)            #Cierre de conexion con MySQL

    except sql.Error as e:
        print("\tError con la conexion MySQL\n".upper(), e)

    resultado=DBconectOK
    return resultado

def openDBconect(propiedadesUsuario):
    resultado=None
    BDexist=0
    db_connection = None        # Variable conector SQL con base de datos
    host_user = propiedadesUsuario[0]
    usuario = propiedadesUsuario[1]
    contra = propiedadesUsuario[2]
    dbName= propiedadesUsuario[3]

    #Establecer Conexion --------------------------------------------------------------------
    try:
        db_connection = sql.connect(
            host=host_user,
            user=usuario,
            passwd=contra,
            database=dbName
        )
        resultado=db_connection
    except sql.Error as e:
        print("\tError con la conexion con base de Datos".upper(), e)
    return (resultado)

def testTablas(db_conexion):
    resultado=[]
    #informacion de la conexion
    if db_conexion.is_connected():
        db_Info = db_conexion.get_server_info()
        db_cursor = db_conexion.cursor()
        db_cursor.execute("select database();")
        record = db_cursor.fetchone()

    #REVISAR EXISTENCIA DE TABLAS
    db_cursor.execute("SHOW TABLES")
    for db in db_cursor:
        resultado.append(db[0])
    return resultado

def testColumnasTablas(db_conexion,nombreTabla):
    resultado=None

    if db_conexion.is_connected():
        db_cursor = db_conexion.cursor()

    try:
        db_cursor.execute("select * from "+str(nombreTabla))
        instacias = db_cursor.fetchall()
        num_atributos = len(db_cursor.description)
        nombres_atributos = [i[0] for i in db_cursor.description]

        resultado=nombres_atributos
        db_conexion.commit()
    except: db_conexion.rollback()

    return resultado

def testLlavesTablas(db_conexion,nombreTabla):
    resultado=[]

    if db_conexion.is_connected():
        db_cursor = db_conexion.cursor()
        query='SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_NAME = \''+ str(nombreTabla) + '\' AND CONSTRAINT_NAME = \'PRIMARY\''
        try:
            db_cursor.execute(query)
            records = db_cursor.fetchall()

            # Showing the data
            for record in records:
                resultado.append(str(record[0]))
            db_conexion.commit()
        except:
            db_conexion.rollback()

    return resultado

def getValorLlavesTablas(db_conexion,nombreTabla,LlavesPrimarias):
    resultado=[]

    if nombreTabla=='paciente_laboratorio':
        stringPrimaryKey=str('folio_orden')
    else:
        stringPrimaryKey = str(LlavesPrimarias[0])

    for i in range(len(LlavesPrimarias)):
        if i>0: stringPrimaryKey=stringPrimaryKey+', '+str(LlavesPrimarias[i])

    if db_conexion.is_connected():
        db_cursor = db_conexion.cursor()
        query='SELECT '+str(stringPrimaryKey)+' FROM '+str(nombreTabla)
        try:
            db_cursor.execute(query)
            records = db_cursor.fetchall()

            # Showing the data
            if records:
                for record in records:
                    resultado.append(record[0])
            else:
                print('Llave primaria sin registros')

            db_conexion.commit()
        except:
            db_conexion.rollback()

    return resultado

def loadDiccATablaSQL(db_conexion,nombreTabla,nombreColumnasTabla,valorLlavesPrimarias,dicc, listaNssNotasIniciales):
    resultado=[]
    listaValoresDic = []

    actualizarBD=False
    totalNuevasLlaves=0

    keysDicGeneral=dicc.keys()
    keysDicGeneral=list(keysDicGeneral)

    valuesSQLstring='%s'
    columnasSQLstring=str(nombreColumnasTabla[0])

    #obtener string de VALUES para consulta SQL
    dicDerivado = dicc[keysDicGeneral[0]]
    keysDicDerivado = dicDerivado.keys()
    keysDicDerivado = list(keysDicDerivado)

        # ADICION PARA NOTAS EGRESO/INTERCONSULTAS
    if nombreTabla== 'paciente_nota_egreso' or nombreTabla=='paciente_nota_inter':
        keysVerificacion=keysDicGeneral.copy()
        for valor in keysVerificacion:
            intValor=float(valor)
            if not intValor in listaNssNotasIniciales:
                dicc.pop(str(valor))
                keysDicGeneral.remove(str(valor))
            else:None

        # ADICION PARA LABORATORIOS
    if nombreTabla=='paciente_laboratorio':
        keysDicDerivado.pop()

    for i in range(len(keysDicDerivado)):
        if i>0:
            valuesSQLstring = valuesSQLstring+', %s'

    for i in range(len(nombreColumnasTabla)):
        if i>0: columnasSQLstring = columnasSQLstring+', '+str(nombreColumnasTabla[i])

    query = 'INSERT INTO ' + str(nombreTabla) + ' ('+str(columnasSQLstring)+') VALUES ('+str(valuesSQLstring)+')'

    if not valorLlavesPrimarias:
        # Actualizar TODAS LAS FILAS DE BD con valores del diccionario
        actualizarBD = True
        for valor in dicc:
            dicDerivado = dicc[valor]
            dicDerivadoCopy=dicDerivado.copy()
            # ADICION PARA LABORATORIOS
            if nombreTabla == 'paciente_laboratorio':
                dicDerivadoCopy.popitem()
                resultado=keysDicGeneral
            dicDerivadoValues = dicDerivadoCopy.values()
            dicDerivadoValues=tuple(dicDerivadoValues)
            listaValoresDic.append(dicDerivadoValues)

    else:
        # Estimar nuevas filas para actualizar en BD
        for key in keysDicGeneral:
            valor=int(key)
            if valor in valorLlavesPrimarias: print('Llave existente en BD: ',valor)
            else:
                actualizarBD=True
                #Se encontro nuevo registro para actualizarse en BD
                print('llave NO existente en BD:', valor)
                totalNuevasLlaves+=1

                dicDerivado = dicc[key]
                dicDerivadoCopy=dicDerivado.copy()
                # ADICION PARA LABORATORIOS
                if nombreTabla == 'paciente_laboratorio':
                    dicDerivadoCopy.popitem()
                    resultado.append(key)
                dicDerivadoValues = dicDerivadoCopy.values()
                dicDerivadoValues=tuple(dicDerivadoValues)
                listaValoresDic.append(dicDerivadoValues)

    db_cursor = db_conexion.cursor()
    if actualizarBD:
        try:
            db_cursor.executemany(query, listaValoresDic)
            db_conexion.commit()

        except sql.Error as e:
            db_conexion.rollback()
    else:
        print('\n\tNo hay nuevos registros para actualizar'.upper())

    return resultado

def loadDiccLabsATablaSQL(db_conexion, nombreTabla, nombreColumnasTabla, valorLlavesFolios, dicc,listaNssNotasIniciales):
    resultado = []
    listaValoresDic = []

    actualizarBD = False

    keysDicNSS = dicc.keys()
    keysDicNSS = list(keysDicNSS)

    valuesSQLstring = '%s'
    columnasSQLstring = str(nombreColumnasTabla[0])

    # obtener string de VALUES para consulta SQL
    diccFolios = dicc[keysDicNSS[0]]
    keysDicFolios=list(diccFolios.keys())

    #DICCIONARIO DERIVADO CON LOS DATOS A GUARDAR
    dicDerivado=diccFolios[keysDicFolios[0]]
    keysDicDerivado = dicDerivado.keys()
    keysDicDerivado = list(keysDicDerivado)
    # ADICION PARA LABORATORIO
    keysDicDerivado.pop()

    for i in range(len(keysDicDerivado)):
        if i > 0:
            valuesSQLstring = valuesSQLstring + ', %s'
  

    for i in range(len(nombreColumnasTabla)):
        if i > 0: columnasSQLstring = columnasSQLstring + ', ' + str(nombreColumnasTabla[i])

    query = 'INSERT INTO ' + str(nombreTabla) + ' (' + str(columnasSQLstring) + ') VALUES (' + str(
        valuesSQLstring) + ')'

    if not valorLlavesFolios:
        # Actualizar TODAS LAS FILAS DE BD con valores del diccionario
        actualizarBD = True
        for valor in dicc:
            if int(valor) in listaNssNotasIniciales:
                diccFolios = dicc[valor]

                for folioActual in diccFolios:
                    dicDerivado = diccFolios[folioActual]
                    dicDerivadoCopy = dicDerivado.copy()
                    # ADICION PARA LABORATORIOS
                    dicDerivadoCopy.popitem()
                    resultado.append(folioActual)

                    dicDerivadoValues = dicDerivadoCopy.values()
                    dicDerivadoValues = tuple(dicDerivadoValues)
                    listaValoresDic.append(dicDerivadoValues)
            else:
                print('\n\tNSS: ',valor,' Sin Registro en Notas Clinicas (SE OMITIRA)\n')

    else:
        # Estimar nuevas filas para actualizar en BD
        for key in keysDicNSS:
            Floatkey=float(key)
            if Floatkey in listaNssNotasIniciales:
                diccFolios = dicc[key]
                keysDicFolios = list(diccFolios.keys())

                for folioActual in keysDicFolios:
                    valor=float(folioActual)

                    if valor in valorLlavesFolios:
                        print('Llave existente en BD: ', valor)
                    else:
                        actualizarBD = True
                        # Se encontro nuevo registro para actualizarse en BD
                        print('llave NO existente en BD:', valor)

                        dicDerivado = diccFolios[folioActual]
                        dicDerivadoCopy = dicDerivado.copy()
                        # ADICION PARA LABORATORIOS
                        dicDerivadoCopy.popitem()
                        resultado.append(folioActual)

                        dicDerivadoValues = dicDerivadoCopy.values()
                        dicDerivadoValues = tuple(dicDerivadoValues)
                        listaValoresDic.append(dicDerivadoValues)
            else: None

    db_cursor = db_conexion.cursor()
    if actualizarBD:
        try:
            db_cursor.executemany(query, listaValoresDic)
            db_conexion.commit()
    
        except sql.Error as e:
            db_conexion.rollback()
    else:
        print('\n\tNo hay nuevos registros para actualizar'.upper())

    return resultado

def loadLaboratorioEstudiosSQL(db_conexion, folioObjetivo, dicc):
    resultado=None
    listaValoresDic=[]
    listaNSSObjetivos=[]
    listaValoresQuery=[]
    nombreTabla=''
    actualizarBD = False

    if folioObjetivo:
        actualizarBD=True
    else: None

    if actualizarBD:
        listaNSSObjetivos = list(dicc.keys())
        valuesSQLstring = '%s, %s, %s, %s, %s, %s'
        columnasSQLstring = 'nss, folio_orden, determinacion, resultado, unidad, valor_normal'


        for nss in listaNSSObjetivos:
            diccFolio={}
            listaFoliosObjetivos=[]

            diccFolio=dicc[str(nss)]
            listaFoliosObjetivos=list(diccFolio.keys())

            for folioActual in listaFoliosObjetivos:
                if folioActual in folioObjetivo:
                    dicDerivado={}
                    dicEstudios={}
                    dicEstudiosKeys={}
                    folioOrden={}
                    listaValoresDic=[]

                    dicDerivado = diccFolio[str(folioActual)]
                    nssInt=int(nss)
                    folioOrden = dicDerivado['folio_orden']
                    dicEstudios=dicDerivado['estudios']
                    dicEstudiosKeys=dicEstudios.keys()
                    dicEstudiosKeys=list(dicEstudiosKeys)

                    for NombreEstudio in dicEstudiosKeys:
                        dicEstudiosDerivado={}
                        dicDerivadoValues=[]
                        listaValoresQuery=[]
                        listaValoresDic=[]

                        nombreTabla=str(NombreEstudio)
                        nombreTabla=nombreTabla.replace(' ','_').replace('-','_')

                        dicEstudiosDerivado=dicEstudios[str(NombreEstudio)]
                        dicDerivadoValues = list(dicEstudiosDerivado.values())
                        for j in range(len(dicDerivadoValues[0])):
                            listaValoresQuery.append(nssInt)
                            listaValoresQuery.append(folioOrden)
                            listaValoresQuery.append(dicDerivadoValues[0][j])
                            listaValoresQuery.append(dicDerivadoValues[1][j])
                            listaValoresQuery.append(dicDerivadoValues[2][j])
                            listaValoresQuery.append(dicDerivadoValues[3][j])
                            tuplaValoresQuery = tuple(listaValoresQuery)
                            listaValoresDic.append(tuplaValoresQuery)
                            listaValoresQuery.clear()

                        query = 'INSERT INTO ' + 'paciente_' + str(nombreTabla) + ' (' + str(columnasSQLstring) + ') VALUES (' + str(valuesSQLstring) + ')'
                        

                        db_cursor = db_conexion.cursor()
                        if actualizarBD:
                            try:
                                db_cursor.executemany(query, listaValoresDic)
                                db_conexion.commit()
                                print("\nRegistro de Estudios Labs a MYSQL exitoso...!")
                            except sql.Error as e:
                                print("\tERROR con la transferencia de datos a MYSQL\n\t".upper(), e)
                                db_conexion.rollback()
                        else: print('\n\tNo hay nuevos registros para actualizar'.upper())
                else: print('\n\tFolio: '+str(folioActual)+', Existente en BD')


    else: print('\n\tNo hay nuevos registros para actualizar')
    return resultado


def DBmanager(diccionarios):
    propiedadesUsuario=["localhost","root","contra","diagnostico_auto"]
    listaTablas=[]
    listaColumnas=[]
    tablaConsulta=''

    registrosNotaInicial=[]

    dicPaciente = diccionarios['Dic_Pacientes']
    dicNotaInicial = diccionarios['Dic_NotaInicial']
    dicLaboratorio = diccionarios['Dic_Laboratorio']
    dicNotaFinal = diccionarios['Dic_NotaEgreso']

    statusMySQL=testMySQLconect(propiedadesUsuario)

    if statusMySQL:
                    #Establecer conexion con Base de Datos
        db_conexion=openDBconect(propiedadesUsuario)

                    #probar existencia de tablas
        listaTablas=testTablas(db_conexion)

                    #consultar datos de tabla 1: pacientes*************************************************************
        tablaConsulta = 'paciente_paciente'
        if  tablaConsulta in listaTablas:
            x=listaTablas.index(tablaConsulta)
            listaColumnas=testColumnasTablas(db_conexion,listaTablas[x])

            # comparar llaves de tabla paciente con existente en diccionario e imprimir resultados
            llavesPrimarias=testLlavesTablas(db_conexion,listaTablas[x])
            valorLlavesPrimarias=getValorLlavesTablas(db_conexion,listaTablas[x],llavesPrimarias)

            #llenar datos de pacientes
            for key,value in dicPaciente.items():
                value['nombre_paciente'] = None

            if dicPaciente:
                loadDiccATablaSQL(db_conexion,listaTablas[x],listaColumnas,valorLlavesPrimarias,dicPaciente,registrosNotaInicial)
            else:
                print('\tNo hay nuevos datos de: ',tablaConsulta,' para guardar en base de datos')
        else: None

                    #consultar datos de tabla 2: nota_inicial*********************************************************
        tablaConsulta = 'paciente_nota_inicial'
        if tablaConsulta in listaTablas:
            x=listaTablas.index(tablaConsulta)
            listaColumnas=testColumnasTablas(db_conexion,listaTablas[x])

            # comparar llaves de tabla paciente con existente en diccionario e imprimir resultados
            llavesPrimarias=testLlavesTablas(db_conexion,listaTablas[x])
            valorLlavesPrimarias=getValorLlavesTablas(db_conexion,listaTablas[x],llavesPrimarias)
            registrosNotaInicial=valorLlavesPrimarias    #comparativa para tablas dependientes

            #llenar datos de pacientes
            if dicNotaInicial:
                loadDiccATablaSQL(db_conexion,listaTablas[x],listaColumnas,valorLlavesPrimarias,dicNotaInicial,registrosNotaInicial)
            else:
                print('\tNo hay nuevos datos de: ',tablaConsulta,' para guardar en base de datos')
        else: None
                    #consultar datos de tabla 3: Laboratorios*********************************************************
        tablaConsulta = 'paciente_laboratorio'

        if  tablaConsulta in listaTablas:

            x=listaTablas.index(tablaConsulta)
            listaColumnas=testColumnasTablas(db_conexion,listaTablas[x])

            # comparar llaves de tabla paciente con existente en diccionario e imprimir resultados
            llavesPrimarias=testLlavesTablas(db_conexion,listaTablas[x])
            valorLlavesPrimarias=getValorLlavesTablas(db_conexion,listaTablas[x],llavesPrimarias)

            if dicLaboratorio:
                # llenar datos de laboratorio
                foliosObjetivo=loadDiccLabsATablaSQL(db_conexion,listaTablas[x],listaColumnas,valorLlavesPrimarias,dicLaboratorio,registrosNotaInicial)
                # consultar datos de tabla 3.2: Laboratorios/Estudios
                if foliosObjetivo: loadLaboratorioEstudiosSQL(db_conexion,foliosObjetivo,dicLaboratorio)
                #loadLaboratorioEstudiosSQL(db_conexion, llavesObjetivo, dicLaboratorio)
            else:
                print('\tNo hay nuevos datos de: ',tablaConsulta,' para guardar en base de datos')
        else:None
                    #Consultar datos de tabla 4: Notas de Egreso******************************************************
        tablaConsulta = 'paciente_nota_egreso'
        if tablaConsulta in listaTablas:
            x=listaTablas.index(tablaConsulta)
            listaColumnas=testColumnasTablas(db_conexion,listaTablas[x])

            # comparar llaves de tabla paciente con existente en diccionario e imprimir resultados
            llavesPrimarias=testLlavesTablas(db_conexion,listaTablas[x])
            valorLlavesPrimarias=getValorLlavesTablas(db_conexion,listaTablas[x],llavesPrimarias)

            #llenar datos de pacientes
            if dicNotaFinal:
                loadDiccATablaSQL(db_conexion,listaTablas[x],listaColumnas,valorLlavesPrimarias,dicNotaFinal,registrosNotaInicial)
            else:
                print('\tNo hay nuevos datos de: ',tablaConsulta,' para guardar en base de datos')
        else: None


        closeDBconect(db_conexion)
    else:
        print('\nError, Favor de revisar especificaciones de conexion con MySQL')
    return None


def DBStatusTables(nombreTabla):
    propiedadesUsuario=["localhost","root","contra","diagnostico_auto"]
    resultado=None    #Primera conexion
    tablaConsulta = nombreTabla

    statusMySQL=testMySQLconect(propiedadesUsuario)

    if statusMySQL:

        #Establecer conexion con Base de Datos
        db_conexion=openDBconect(propiedadesUsuario)

        #Obtener valores existentes de llaves
        llavesPrimarias = testLlavesTablas(db_conexion, tablaConsulta)
        valorLlavesPrimarias=getValorLlavesTablas(db_conexion,tablaConsulta,llavesPrimarias)

        resultado=valorLlavesPrimarias.copy()

        closeDBconect(db_conexion)
    else:
        print('\nError, Favor de revisar especificaciones de conexion con MySQL')

    return resultado