from django.urls import path
from .views import register, login, patient, get_patient_by_id, doctor, doctor_by_id, mapping, get_doctors_by_patient

urlpatterns = [
    path('auth/register/',register,name='register'),
    path('auth/login/',login,name='Login'),
    path('patients/', patient , name='patient'),
    path('patients/<id>/',get_patient_by_id,name='patient_by_id'),
    path('doctors/',doctor , name='doctors'),
    path('doctors/<id>/',doctor_by_id,name='doctor_by_id'),
    path('mappings/',mapping,name='mapping'),
    path('mappings/<patient_id>/',get_doctors_by_patient,name='all_dr_to_patient'),
]