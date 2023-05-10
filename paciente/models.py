from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Paciente(models.Model):
    nss = models.FloatField(null=False, unique=True, primary_key=True)#Numero de seguro social
    nombre_paciente = models.CharField(max_length=250, null=True, blank=True)

class Nota_inicial(models.Model):
    nss = models.FloatField(null=False, unique=True, primary_key=True)#Numero de seguro social
    fecha_ingreso = models.DateField(null=False)
    genero = models.CharField(max_length=5, null=True, blank=True)
    especialidad_ingreso = models.CharField(max_length=500, null=True, blank=True)
    motivo_inter = models.CharField(max_length=250, null=True, blank=True)
    interrogatorio = models.TextField(null=True, blank=True)
    dx = models.CharField(max_length=500, null=True, blank=True)
    plan_tratamiento = models.TextField(null=True, blank=True)
    pronostico = models.CharField(max_length=1000, null=True, blank=True)
    indicaciones = models.TextField(null=True, blank=True)
    estado_salud = models.CharField(max_length=50, null=True, blank=True)
    peso = models.FloatField(null=True, blank=True)
    talla = models.FloatField(null=True, blank=True)
    temperatura = models.FloatField(null=True, blank=True)
    frec_respiratoria = models.FloatField(null=True, blank=True)
    frec_cardiaca = models.FloatField(null=True, blank=True)
    pres_arterial = models.CharField(max_length=10, null=True, blank=True)
    imc = models.FloatField(null=True, blank=True)
    saturacion = models.FloatField(null=True, blank=True)
    glc_capilar = models.FloatField(null=True, blank=True)
    diagnostico_inicial = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nss', 'fecha_ingreso'], name='unique_migration_Nota_inicial'
            )
        ]

class Nota_egreso(models.Model):
    nss = models.FloatField(null=False, unique=True, primary_key=True)#Numero de seguro social
    fecha_ingreso = models.DateField(null=True, blank=True)
    fecha_egreso = models.DateField(null=False)
    especialidad_egreso = models.CharField(max_length=500, null=True, blank=True)
    motivo_egreso = models.CharField(max_length=500, null=True, blank=True)
    envio = models.CharField(max_length=250, null=True, blank=True)
    diagnostico_ingreso = models.CharField(max_length=800, null=True, blank=True)
    diagnostico_egreso = models.CharField(max_length=800, null=True, blank=True)
    resumen_evolucion = models.TextField(null=True, blank=True)
    problemas_pendientes = models.TextField(null=True, blank=True)
    plan_tratamiento = models.TextField(null=True, blank=True)
    recomendaciones = models.CharField(max_length=500, null=True, blank=True)
    factores_riesgo = models.CharField(max_length=500, null=True, blank=True)
    pronostico = models.CharField(max_length=500, null=True, blank=True)
    diagnostico_defuncion = models.CharField(max_length=500, null=True, blank=True)
    estado_salud = models.CharField(max_length=50, null=True, blank=True)
    peso = models.FloatField(null=True, blank=True)
    talla = models.FloatField(null=True, blank=True)
    temperatura = models.FloatField(null=True, blank=True)
    frec_respiratoria = models.FloatField(null=True, blank=True)
    frec_cardiaca = models.FloatField(null=True, blank=True)
    pres_arterial = models.CharField(max_length=10, null=True, blank=True)
    imc = models.FloatField(null=True, blank=True)
    saturacion = models.FloatField(null=True, blank=True)
    glc_capilar = models.FloatField(null=True, blank=True)
    diagnostico_final = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nss', 'fecha_egreso'], name='unique_migration_Nota_egreso'
            )
        ]

class Pruebas_especiales(models.Model):
    nss = models.FloatField(null=False, unique=True, primary_key=True)#Numero de seguro social
    folio_orden = models.FloatField(null=False)
    determinacion = models.CharField(max_length=100, null=False)
    resultado = models.CharField(max_length=100, null=True, blank=True)
    unidad = models.CharField(max_length=100, null=True, blank=True)
    valor_normal = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nss', 'folio_orden','determinacion'], name='unique_migration_Pruebas_especiales'
            )
        ]

class Quimica_clinica(models.Model):
    nss = models.FloatField(null=False, unique=True, primary_key=True)#Numero de seguro social
    folio_orden = models.FloatField(null=False)
    determinacion = models.CharField(max_length=100, null=False)
    resultado = models.CharField(max_length=100, null=True, blank=True)
    unidad = models.CharField(max_length=100, null=True, blank=True)
    valor_normal = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nss', 'folio_orden','determinacion'], name='unique_migration_Quimica_clinica'
            )
        ]

class Medicina_nuclear(models.Model):
    nss = models.FloatField(null=False, unique=True, primary_key=True)#Numero de seguro social
    folio_orden = models.FloatField(null=False)
    determinacion = models.CharField(max_length=100, null=False)
    resultado = models.CharField(max_length=100, null=True, blank=True)
    unidad = models.CharField(max_length=100, null=True, blank=True)
    valor_normal = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nss', 'folio_orden','determinacion'], name='unique_migration_Medicina_nuclear'
            )
        ]

class Laboratorio(models.Model):
    nss = models.FloatField(null=False, unique = True,primary_key=True)#Numero de seguro social
    folio_orden = models.FloatField(null=False,unique = True)
    fecha_orden = models.DateField(null=True, blank=True)
    edad = models.PositiveIntegerField(null=True,blank=True)
    servicio_solicita = models.CharField(max_length=250, null=True,blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nss', 'folio_orden'], name='unique_migration_host_combination'
            )
        ]

class Inmunologia(models.Model):
    nss = models.FloatField(null=False, unique=True, primary_key=True)#Numero de seguro social
    folio_orden = models.FloatField(null=False)
    determinacion = models.CharField(max_length=100, null=False)
    resultado = models.CharField(max_length=100, null=True, blank=True)
    unidad = models.CharField(max_length=100, null=True, blank=True)
    valor_normal = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nss', 'folio_orden','determinacion'], name='unique_migration_Inmunologia'
            )
        ]

class Inmuno_infecto(models.Model):
    nss = models.FloatField(null=False, unique=True, primary_key=True)#Numero de seguro social
    folio_orden = models.FloatField(null=False)
    determinacion = models.CharField(max_length=100, null=False)
    resultado = models.CharField(max_length=100, null=True, blank=True)
    unidad = models.CharField(max_length=100, null=True, blank=True)
    valor_normal = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nss', 'folio_orden','determinacion'], name='unique_migration_Inmuno_infecto'
            )
        ]

class Hematologia(models.Model):
    nss = models.FloatField(null=False, unique=True, primary_key=True)#Numero de seguro social
    folio_orden = models.FloatField(null=False)
    determinacion = models.CharField(max_length=100, null=False)
    resultado = models.CharField(max_length=100, null=True, blank=True)
    unidad = models.CharField(max_length=100, null=True, blank=True)
    valor_normal = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nss', 'folio_orden','determinacion'], name='unique_migration_Hematologia'
            )
        ]

class Drogas_terapeuticas(models.Model):
    nss = models.FloatField(null=False, unique=True, primary_key=True)#Numero de seguro social
    folio_orden = models.FloatField(null=False)
    determinacion = models.CharField(max_length=100, null=False)
    resultado = models.CharField(max_length=100, null=True, blank=True)
    unidad = models.CharField(max_length=100, null=True, blank=True)
    valor_normal = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nss', 'folio_orden','determinacion'], name='unique_migration_Drogas_terapeuticas'
            )
        ]

class Coagulaciones(models.Model):
    nss = models.FloatField(null=False, unique=True, primary_key=True)#Numero de seguro social
    folio_orden = models.FloatField(null=False)
    determinacion = models.CharField(max_length=100, null=False)
    resultado = models.CharField(max_length=100, null=True, blank=True)
    unidad = models.CharField(max_length=100, null=True, blank=True)
    valor_normal = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nss', 'folio_orden','determinacion'], name='unique_migration_Coagulaciones'
            )
        ]