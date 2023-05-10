from xml.dom.minidom import Document
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    HomePageView,
    PacienteCreateView, 
    Nota_inicialCreateView,
    addrecordnotainicial,
    Nota_egresoCreateView,
    addrecordnotaegreso,
    Pruebas_especialesCreateView,
    addrecordpruebasespeciales,
    Quimica_clinicaCreateView,
    addrecordquimicaclinica,
    Medicina_nuclearCreateView,
    addrecordmedicinanuclear,
    LaboratorioCreateView,
    addrecordlaboratorio,
    InmunologiaCreateView,
    addrecordInmunologia,
    Inmuno_infectoCreateView,
    addrecordinmunoinfecto,
    HematologiaCreateView,
    addrecordhematologia,
    Drogas_terapeuticasCreateView,
    addrecorddrogasterapeuticas,
    CoagulacionesCreateView,
    addrecordcoagulaciones,
    
    SearchPacienteListView,
    PacienteDetailView,
    Nota_inicialDetailView,
    Nota_egresoDetailView,
    Pruebas_especialesDetailView,
    Quimica_clinicaDetailView,
    Medicina_nuclearDetailView,
    LaboratorioDetailView,
    InmunologiaDetailView,
    Inmuno_infectoDetailView,
    HematologiaDetailView,
    Drogas_terapeuticasDetailView,
    CoagulacionesDetailView,
    PacienteEditView,
    PacienteDeleteView,
    upload,

    SearchNotaInicialListView,
    SearchNotaEgresoListView,
    SearchPruebasEspecialesListView,
    SearchQuimicaclinicaListView,
    SearcMedicinanuclearListView,
    SearcLaboratorioListView,
    SearcInmunologiaListView,
    SearcinmunoinfectoListView,
    SearchematologiaListView,
    SearchdrogasterapeuticasListView,
    SearchcoagulacionesListView,

    updatequimicaclinica,
    updaterecordquimicaclinica,
    deletequimicaclinica,
    updatepruebasespeciales,
    updaterecordpruebasespeciales,
    deletepruebasespeciales,
    updatemedicinanuclear,
    updaterecordmedicinanuclear,
    deletemedicinanuclear,
    updatelaboratorio,
    updaterecordlaboratorio,
    deletelaboratorio,
    updateinmunologia,
    updaterecordinmunologia,
    deleteinmunologia,
    updateinmunoinfecto,
    updaterecordinmunoinfecto,
    deleteinmunoinfecto,
    updatehematologia,
    updaterecordhematologia,
    deletehematologia,
    updatedrogasterapeuticas,
    updaterecorddrogasterapeuticas,
    deletedrogasterapeuticas,
    updatecoagulaciones,
    updaterecordcoagulaciones,
    deletecoagulaciones,
    updatenotaegreso,
    updaterecordnotaegreso,
    deletenotaegreso,
    updatenotainicial,
    updaterecordnotainicial,
    deletenotainicial,
    DetallesView
)

urlpatterns = [
    path('', HomePageView.as_view(), name='pacientes'), #agrega un paciente
    path('nuevo_paciente/', PacienteCreateView.as_view(), name='nuevo_paciente'), #agrega un paciente

    path('<str:nss>/nueva_nota_inicial/', Nota_inicialCreateView, name='nueva_nota_inicial'), #agrega un nueva_nota_inicial
    path('<str:nss>/nueva_nota_inicial/addrecord/', addrecordnotainicial, name='addrecord'), #agrega un nueva_nota_inicial

    path('<str:nss>/nueva_nota_egreso/', Nota_egresoCreateView, name='nueva_nota_egreso'), #agrega un nueva_nota_egreso
    path('<str:nss>/nueva_nota_egreso/addrecord/', addrecordnotaegreso, name='addrecord'), #agrega un nueva_nota_egreso

    path('<str:nss>/nueva_pruebas_especiales/', Pruebas_especialesCreateView, name='nueva_pruebas_especiales'), #agrega un nueva_Pruebas_especiales
    path('<str:nss>/nueva_pruebas_especiales/addrecord/', addrecordpruebasespeciales, name='addrecord'), #agrega un nueva_Pruebas_especiales

    path('<str:nss>/nueva_quimica_clinica/', Quimica_clinicaCreateView, name='nueva_quimica_clinica'), #agrega un nueva_Quimica_clinica
    path('<str:nss>/nueva_quimica_clinica/addrecord/', addrecordquimicaclinica, name='addrecord'), #agrega un nueva_Quimica_clinica

    path('<str:nss>/nueva_medicina_nuclear/', Medicina_nuclearCreateView, name='nueva_medicina_nuclear'), #agrega un nueva_Medicina_nuclear
    path('<str:nss>/nueva_medicina_nuclear/addrecord/', addrecordmedicinanuclear, name='addrecord'), #agrega un medicina_nuclear

    path('<str:nss>/nueva_laboratorio/', LaboratorioCreateView, name='nueva_laboratorio'), #agrega un nueva_Laboratorio
    path('<str:nss>/nueva_laboratorio/addrecord/', addrecordlaboratorio, name='addrecord'), #agrega un Laboratorior

    path('<str:nss>/nueva_inmunologia/', InmunologiaCreateView, name='nueva_inmunologia'), #agrega un Inmunologia
    path('<str:nss>/nueva_inmunologia/addrecord/', addrecordInmunologia, name='addrecord'), #agrega un Inmunologia

    path('<str:nss>/nueva_inmuno_infecto/', Inmuno_infectoCreateView, name='nueva_inmuno_infecto'), #agrega un Inmuno_infecto
    path('<str:nss>/nueva_inmuno_infecto/addrecord/', addrecordinmunoinfecto, name='addrecord'), #agrega un Inmuno infecto

    path('<str:nss>/nueva_hematologia/', HematologiaCreateView, name='nueva_hematologia'), #agrega un Hematologia
    path('<str:nss>/nueva_hematologia/addrecord/', addrecordhematologia, name='addrecord'), #agrega un Inmuno infecto

    path('<str:nss>/nueva_coagulaciones/', CoagulacionesCreateView, name='nueva_coagulaciones'), #agrega un Coagulaciones
    path('<str:nss>/nueva_coagulaciones/addrecord/', addrecordcoagulaciones, name='addrecord'), #agrega un Inmuno infecto

    path('<str:nss>/nueva_drogas_terapeuticas/', Drogas_terapeuticasCreateView, name='nueva_drogas_terapeuticas'), #agrega un Drogas_terapeuticas
    path('<str:nss>/nueva_drogas_terapeuticas/addrecord/', addrecorddrogasterapeuticas, name='addrecord'), #agrega un Inmuno infecto

    path('search/', SearchPacienteListView.as_view(),name='search_pacientes'), #Lista de pacientes del buscador
    path('<str:pk>/search_nota_inicial/', SearchNotaInicialListView.as_view(),name='search_nota_inicial'), #Lista de pacientes del buscador
    path('<str:pk>/search_nota_egreso/', SearchNotaEgresoListView.as_view(),name='search_nota_egreso'), #Lista de pacientes del buscador
    path('<str:pk>/search_pruebas_especiales/', SearchPruebasEspecialesListView.as_view(),name='search_pruebas_especiales'), #Lista de pacientes del buscador
    path('<str:pk>/search_quimica_clinica/', SearchQuimicaclinicaListView.as_view(),name='search_quimica_clinica'),
    path('<str:pk>/search_medicina_nuclear/', SearcMedicinanuclearListView.as_view(),name='search_medicina_nuclear'),
    path('<str:pk>/search_laboratorio/', SearcLaboratorioListView.as_view(),name='search_laboratorio'),
    path('<str:pk>/search_inmunologia/', SearcInmunologiaListView.as_view(),name='search_inmunologia'),
    path('<str:pk>/search_inmuno_infecto/', SearcinmunoinfectoListView.as_view(),name='search_inmuno_infecto'),
    path('<str:pk>/search_hematologia/', SearchematologiaListView.as_view(),name='search_hematologia'),
    path('<str:pk>/search_drogas_terapeuticas/', SearchdrogasterapeuticasListView.as_view(),name='search_drogas_terapeuticas'),
    path('<str:pk>/search_coagulaciones/', SearchcoagulacionesListView.as_view(),name='search_coagulaciones'),

    path('<str:pk>/detail/',PacienteDetailView.as_view(), name='paciente_detail'),#detalles de paciente

    path('detail_nota_inicial/',Nota_inicialDetailView.as_view(), name='detail_nota_inicial'),#detalles de nota inicial
    path('detail_nota_egreso/',Nota_egresoDetailView.as_view(), name='detail_nota_egreso'),#detalles de nota egreso
    path('detail_pruebas_especiales/',Pruebas_especialesDetailView.as_view(), name='detail_pruebas_especiales'),#detalles de Pruebas_especiales
    path('detail_quimica_clinica/',Quimica_clinicaDetailView.as_view(), name='detail_quimica_clinica'),#detalles de Pruebas_especiales
    path('detail_medicina_nuclear/',Medicina_nuclearDetailView.as_view(), name='detail_medicina_nuclear'),#detalles de Pruebas_especiales
    path('detail_laboratorio/',LaboratorioDetailView.as_view(), name='detail_laboratorio'),#detalles de Pruebas_especiales
    path('detail_inmunologia/',InmunologiaDetailView.as_view(), name='detail_inmunologia'),#detalles de Pruebas_especiales
    path('detail_inmuno_infecto/',Inmuno_infectoDetailView.as_view(), name='detail_inmuno_infecto'),#detalles de Pruebas_especiales
    path('detail_hematologia/',HematologiaDetailView.as_view(), name='detail_hematologia'),#detalles de Pruebas_especiales
    path('detail_drogas_terapeuticas/',Drogas_terapeuticasDetailView.as_view(), name='detail_drogas_terapeuticas'),#detalles de Pruebas_especiales
    path('detail_coagulaciones/',CoagulacionesDetailView.as_view(), name='detail_coagulaciones'),#detalles de Pruebas_especiales

    path('<str:pk>/edit_Paciente/', PacienteEditView.as_view(), name='edit_Paciente'), #
    path('<str:nss>/<str:fecha_ingreso>/editNota_inicial/', updatenotainicial, name='editNota_inicial'),
    path('<str:nss>/<str:fecha_ingreso>/editNota_inicial/updaterecord/', updaterecordnotainicial, name='updaterecord'),

    path('<str:nss>/<str:fecha_egreso>/editNota_egreso/', updatenotaegreso, name='editNota_egreso'),
    path('<str:nss>/<str:fecha_egreso>/editNota_egreso/updaterecord/', updaterecordnotaegreso, name='updaterecord'),

    path('<str:nss>/<str:folio_orden>/<str:determinacion>/editPruebas_especiales/', updatepruebasespeciales, name='editPruebas_especiales'),
    path('<str:nss>/<str:folio_orden>/<str:determinacion>/editPruebas_especiales/updaterecord/', updaterecordpruebasespeciales, name='updaterecordPruebas_especiales'),

    path('<str:nss>/<str:folio_orden>/<str:determinacion>/editQuimica_clinica/', updatequimicaclinica, name='editQuimica_clinica'),
    path('<str:nss>/<str:folio_orden>/<str:determinacion>/editQuimica_clinica/updaterecord/', updaterecordquimicaclinica, name='updaterecord'),

    path('<str:nss>/<str:folio_orden>/<str:determinacion>/editMedicina_nuclear/', updatemedicinanuclear, name='editMedicina_nuclear'),
    path('<str:nss>/<str:folio_orden>/<str:determinacion>/editMedicina_nuclear/updaterecord/', updaterecordmedicinanuclear, name='updaterecord'),

    path('<str:nss>/<str:folio_orden>/editLaboratorio/', updatelaboratorio, name='editLaboratorio'),
    path('<str:nss>/<str:folio_orden>/editLaboratorio/updaterecord/', updaterecordlaboratorio, name='updaterecord'),

    path('<str:nss>/<str:folio_orden>/<str:determinacion>/editInmunologia/', updateinmunologia, name='editInmunologia'),
    path('<str:nss>/<str:folio_orden>/<str:determinacion>/editInmunologia/updaterecord/', updaterecordinmunologia, name='updaterecord'),

    path('<str:nss>/<str:folio_orden>/<str:determinacion>/editInmuno_infecto/', updateinmunoinfecto, name='editInmuno_infecto'),
    path('<str:nss>/<str:folio_orden>/<str:determinacion>/editInmuno_infecto/updaterecord/', updaterecordinmunoinfecto, name='updaterecord'),

    path('<str:nss>/<str:folio_orden>/<str:determinacion>/editHematologia/', updatehematologia, name='editHematologia'),
    path('<str:nss>/<str:folio_orden>/<str:determinacion>/editHematologia/updaterecord/', updaterecordhematologia, name='updaterecord'),

    path('<str:nss>/<str:folio_orden>/<str:determinacion>/editDrogas_terapeuticas/', updatedrogasterapeuticas, name='editDrogas_terapeuticas'),
    path('<str:nss>/<str:folio_orden>/<str:determinacion>/editDrogas_terapeuticas/updaterecord/', updaterecorddrogasterapeuticas, name='updaterecord'),

    path('<str:nss>/<str:folio_orden>/<str:determinacion>/editCoagulaciones/', updatecoagulaciones, name='editCoagulaciones'),
    path('<str:nss>/<str:folio_orden>/<str:determinacion>/editCoagulaciones/updaterecord/', updaterecordcoagulaciones, name='updaterecord'),

    path('<str:pk>/delete_Paciente/', PacienteDeleteView.as_view(), name='delete_Paciente'), #
    path('<str:nss>/<str:fecha_ingreso>/delete_Nota_inicial/', deletenotainicial, name='delete_Nota_inicial'), #
    path('<str:nss>/<str:fecha_egreso>/delete_Nota_egreso/', deletenotaegreso, name='delete_Nota_egreso'), #
    path('<str:nss>/<str:folio_orden>/<str:determinacion>/delete_Pruebas_especiales/', deletepruebasespeciales, name='delete_Pruebas_especiales'), #
    path('<str:nss>/<str:folio_orden>/<str:determinacion>/delete_Quimica_clinica/', deletequimicaclinica, name='delete_Quimica_clinica'), #
    path('<str:nss>/<str:folio_orden>/<str:determinacion>/delete_Medicina_nuclear/', deletemedicinanuclear, name='delete_Medicina_nuclear'), #
    path('<str:nss>/<str:folio_orden>/delete_Laboratorio/', deletelaboratorio, name='delete_Laboratorio'), #
    path('<str:nss>/<str:folio_orden>/<str:determinacion>/delete_Inmunologia/', deleteinmunologia, name='delete_Inmunologia'), #
    path('<str:nss>/<str:folio_orden>/<str:determinacion>/delete_Inmuno_infecto/', deleteinmunoinfecto, name='delete_Inmuno_infecto'), #
    path('<str:nss>/<str:folio_orden>/<str:determinacion>/delete_Hematologia/', deletehematologia, name='delete_Hematologia'), #
    path('<str:nss>/<str:folio_orden>/<str:determinacion>/delete_Drogas_terapeuticas/', deletedrogasterapeuticas, name='delete_Drogas_terapeuticas'), #
    path('<str:nss>/<str:folio_orden>/<str:determinacion>/delete_Coagulaciones/', deletecoagulaciones, name='delete_Coagulaciones'), #

    path('upload/',upload.as_view(),name='upload'),
    path('detalles/',DetallesView.as_view(),name='detalles'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)