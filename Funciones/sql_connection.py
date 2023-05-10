import mysql.connector as sql
import Funciones.data_organize as dataO

def closeDBconect(db_connection):
    db_connection.close()
    return None

def openDBconect(propiedadesUsuario):
    resultado=None
    BDexist=0
    db_connection = None        # Variable conector SQL con base de datos
    host_user = propiedadesUsuario[0]
    usuario = propiedadesUsuario[1]
    contra = propiedadesUsuario[2]
    dbName= propiedadesUsuario[3]

    #Establecer Conexion -----------------------------------------------------------------------------------------------
    try:
        db_connection = sql.connect(
            host=host_user,
            user=usuario,
            passwd=contra,
            database=dbName
        )
        resultado=db_connection
    except sql.Error as e:
        print("\n\tError con la conexion con base de Datos".upper(), e)
    return (resultado)

#______________________________________________________________________________________________________________________
def extract_determinacion_from_study_MYSQL(db_connection,destino):
    resultado=[]

    query='select determinacion from '+destino+' group by determinacion'

    if db_connection.is_connected():
        db_cursor = db_connection.cursor()
    try:
        db_cursor.execute(query)
        instancias = db_cursor.fetchall()
        for i in range(len(instancias)):
            resultado.append(instancias[i][0])

        db_connection.commit()
    except sql.Error as e:
        db_connection.rollback()

    return resultado

def join_study_tables_MYSQL(db_connection,listSelect,listFrom,listOn,listDeterminacion):
    resultado=[]
    strSelect=''
    query=''
    strDeterminacion=''
    strWhere='determinacion='+str(strDeterminacion)

    for valor in listSelect:
        if valor==listSelect[-1]:
            strSelect=strSelect+str(valor)
        else:
            strSelect = strSelect + str(valor)+", "

    for i in range(len(listDeterminacion)):
        query = 'SELECT ' + strSelect + " FROM " + str(listFrom[0])
        querySub = ''
        strWhere=''

        for j in range(1, len(listFrom)):
            querySub = str(querySub) + ' INNER JOIN ' + str(listFrom[j]) + ' ON ' + str(listOn[j - 1])

        strWhere = 'determinacion=\'' + str(listDeterminacion[i])+'\''
        query = 'SELECT ' + strSelect + " FROM " + str(listFrom[0]) + str(querySub) + ' WHERE ' + str(strWhere)

        if db_connection.is_connected():
            db_cursor = db_connection.cursor()

        if i==0:
            try:
                db_cursor.execute(query)
                instancias = db_cursor.fetchall()
                num_atributos = len(db_cursor.description)
                nombres_atributos = [i[0] for i in db_cursor.description]
                resultado=[nombres_atributos,instancias]
                db_connection.commit()
            except sql.Error as e:
                db_connection.rollback()
        else:
            try:
                db_cursor.execute(query)
                Subinstancias = db_cursor.fetchall()
                instancias.extend(Subinstancias)
                num_atributos = len(db_cursor.description)
                nombres_atributos = [i[0] for i in db_cursor.description]
                resultado=[nombres_atributos,instancias]
                db_connection.commit()
            except sql.Error as e:
                db_connection.rollback()

    return resultado

def join_multiple_study_data_from_MYSQL(db_connection,listStudies):
    resultado=[]
    lista_determinacaion=[]
    lista_determinacaiones_totales=[]
    tablas_unidas_totales= [[],[]]

    for estudio in listStudies:
        listSelect = ['paciente_nota_inicial.nss','paciente_nota_inicial.genero','paciente_nota_inicial.peso','paciente_nota_inicial.talla','paciente_nota_inicial.temperatura',
                      'paciente_nota_inicial.frec_respiratoria','paciente_nota_inicial.frec_cardiaca','paciente_nota_inicial.pres_arterial','paciente_nota_inicial.imc',
                      'paciente_nota_inicial.saturacion','paciente_nota_inicial.glc_capilar','paciente_laboratorio.folio_orden','paciente_nota_inicial.fecha_ingreso',
                      estudio+'.determinacion',estudio+'.resultado','paciente_laboratorio.edad']

        listFrom = ['paciente_nota_inicial', 'paciente_laboratorio', estudio]
        listOn = ['paciente_nota_inicial.nss=paciente_laboratorio.nss',
                  'paciente_laboratorio.folio_orden='+estudio+'.folio_orden']

        lista_determinacaion=extract_determinacion_from_study_MYSQL(db_connection,estudio)
        tablas_unidas = join_study_tables_MYSQL(db_connection, listSelect, listFrom, listOn, lista_determinacaion)

        lista_determinacaiones_totales.extend(lista_determinacaion)
        tablas_unidas_totales[0]=tablas_unidas[0].copy()
        tablas_unidas_totales[1].extend(tablas_unidas[1].copy())

    datos_estructurados = dataO.structure_study_data_frame(tablas_unidas_totales,lista_determinacaiones_totales)
    resultado = datos_estructurados
    return resultado
#______________________________________________________________________________________________________________________









def recolectar_datos(db_conexion):
    resultado=None

    query='SELECT paciente_nota_inicial.nss AS \'nss_ingreso\', paciente_nota_inicial.diagnostico_inicial, nota_egreso.diagnostico_final, paciente_nota_inicial.genero, paciente_nota_inicial.interrogatorio AS \'interrogatorio_inicial\', nota_egreso.resumen_evolucion AS \'interrogatorio_final\' FROM paciente_nota_inicial INNER JOIN paciente_laboratorio ON paciente_nota_inicial.nss=paciente_laboratorio.nss INNER JOIN nota_egreso ON paciente_nota_inicial.nss=nota_egreso.nss WHERE diagnostico_final=\'embolia\' OR diagnostico_final=\'neumonia\' OR diagnostico_final=\'control\' GROUP BY paciente_nota_inicial.nss ORDER BY diagnostico_final'

    if db_conexion.is_connected():
        db_cursor = db_conexion.cursor()
    try:
        db_cursor.execute(query)
        instancias = db_cursor.fetchall()
        num_atributos = len(db_cursor.description)
        nombres_atributos = [i[0] for i in db_cursor.description]
        resultado = [nombres_atributos, instancias]
        db_conexion.commit()
        print('\n\tConsulta JOIN de MYSQL exitoso')
    except sql.Error as e:
        print('\n\tERROR con la consulta de datos a MYSQL\n\t'.upper(), e)
        db_conexion.rollback()

    return resultado


def recolectar_labs(db_conexion):
    resultado= None
    ListEstudios = ['paciente_hematologia', 'paciente_coagulaciones', 'paciente_inmuno_infecto', 'paciente_inmunologia', 'paciente_quimica_clinica']

    if db_conexion.is_connected():
        try:
            datalab_raw = join_multiple_study_data_from_MYSQL(db_conexion,ListEstudios)
            db_conexion.commit()
            print('\n\tConsulta JOIN de MYSQL exitoso')
        except sql.Error as e:
            print('\n\tERROR con la consulta de datos a MYSQL\n\t'.upper(), e)
            db_conexion.rollback()

    resultado=datalab_raw
    return resultado

def recolectar_labs2(db_conexion):
    resultado= None
    ListEstudios = ['paciente_hematologia', 'paciente_coagulaciones', 'paciente_inmuno_infecto', 'paciente_inmunologia', 'paciente_quimica_clinica']

    if db_conexion.is_connected():
        try:
            datalab_raw = join_multiple_study_data_from_MYSQL2(db_conexion,ListEstudios)
            db_conexion.commit()
            print('\n\tConsulta JOIN de MYSQL exitoso')
        except sql.Error as e:
            print('\n\tERROR con la consulta de datos a MYSQL\n\t'.upper(), e)
            db_conexion.rollback()

    resultado=datalab_raw
    return resultado

def join_multiple_study_data_from_MYSQL2(db_connection,listStudies):
    resultado=[]
    lista_determinacaion=[]
    lista_determinacaiones_totales=[]
    tablas_unidas_totales= [[],[]]

    for estudio in listStudies:
        listSelect = ['paciente_nota_inicial.nss','paciente_nota_inicial.genero','paciente_nota_inicial.peso','paciente_nota_inicial.talla','paciente_nota_inicial.temperatura',
                      'paciente_nota_inicial.frec_respiratoria','paciente_nota_inicial.frec_cardiaca','paciente_nota_inicial.pres_arterial','paciente_nota_inicial.imc',
                      'paciente_nota_inicial.saturacion','paciente_nota_inicial.glc_capilar','paciente_laboratorio.folio_orden','paciente_laboratorio.edad',
                      estudio+'.determinacion',estudio+'.resultado','paciente_nota_inicial.diagnostico_inicial','paciente_nota_egreso.diagnostico_final', 'paciente_nota_inicial.fecha_ingreso']

        listFrom = ['paciente_nota_inicial', 'paciente_laboratorio','paciente_nota_egreso', estudio]
        listOn = ['paciente_nota_inicial.nss=paciente_laboratorio.nss',
                  'paciente_nota_inicial.nss=paciente_nota_egreso.nss ',
                  'paciente_laboratorio.folio_orden='+estudio+'.folio_orden']

        lista_determinacaion=extract_determinacion_from_study_MYSQL(db_connection,estudio)
        tablas_unidas = join_study_tables_MYSQL(db_connection, listSelect, listFrom, listOn, lista_determinacaion)

        lista_determinacaiones_totales.extend(lista_determinacaion)
        tablas_unidas_totales[0]=tablas_unidas[0].copy()
        tablas_unidas_totales[1].extend(tablas_unidas[1].copy())

    datos_estructurados = dataO.structure_study_data_frame2(tablas_unidas_totales,lista_determinacaiones_totales)
    resultado = datos_estructurados
    return resultado