from django import forms
from .models import IncidentReport

class IncidentReportForm(forms.ModelForm):
    PROOF_CHOICES = [
        ('none', 'None'),
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video')
    ]

    proof_type = forms.ChoiceField(choices=PROOF_CHOICES, required=False, label='Proof Type')

    class Meta:
        model = IncidentReport
        fields = ['title', 'description', 'report_type', 'public_share_level', 'police_station', 'case_number', 'proof_type','location']
