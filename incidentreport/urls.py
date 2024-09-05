from django.urls import path
from . import views
app_name = 'incidentreport'
urlpatterns = [
    path('incident-report' , views.incident_report , name='incident-report'),
]