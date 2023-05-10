from django import forms
from django.forms import fields
from .models import Nota_inicial, Laboratorio

class PacientesForm(forms.ModelForm):
    class Meta:
        model = Nota_inicial
        fields = ('nss','fecha_ingreso','genero','especialidad_ingreso','motivo_inter','interrogatorio','dx','plan_tratamiento','pronostico',
        'indicaciones','estado_salud','peso','talla','temperatura','frec_respiratoria','frec_cardiaca','pres_arterial','imc','saturacion','glc_capilar',
        'diagnostico_inicial',)

class LabortorioForm(forms.ModelForm):
    class Meta:
        model= Laboratorio
        fields = ('nss','folio_orden','fecha_orden','edad','servicio_solicita')

class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))