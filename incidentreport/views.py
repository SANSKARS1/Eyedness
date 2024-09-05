from django.shortcuts import render, redirect
from .forms import IncidentReportForm
from .models import MediaFile, IncidentReport
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def incident_report(request):
    if request.method == 'POST':
        report_form = IncidentReportForm(request.POST)
        if report_form.is_valid():
            # Save the incident report
            incident_report = report_form.save()

            # Get the proof type from the form
            proof_type = report_form.cleaned_data['proof_type']

            # Handle file uploads based on the proof type
            if proof_type in ['image', 'audio', 'video']:
                files = request.FILES.getlist('files')
                allowed_types = {
                    'image': ['image/jpeg', 'image/png'],
                    'audio': ['audio/mpeg', 'audio/wav'],
                    'video': ['video/mp4', 'video/x-msvideo']
                }

                for file in files:
                    if file.content_type in allowed_types[proof_type]:
                        MediaFile.objects.create(incident_report=incident_report, file=file)
                    else:
                        messages.error(request, f"{file.name} is not a valid file for {proof_type}.")
            else:
                messages.info(request, 'No files uploaded for the selected proof type.')

            return redirect('home')
    else:
        report_form = IncidentReportForm()

    return render(request, 'incidentreport/incident_report.html', {'report_form': report_form})
