from django.db import models
class IncidentReport(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    report_type = models.CharField(max_length=50, choices=[('public', 'Public Share'), ('police', 'Police Report')])
    public_share_level = models.CharField(max_length=50, choices=[('public', 'Public'), ('community', 'Community')], blank=True, null=True)
    police_station = models.CharField(max_length=255, blank=True, null=True)
    case_number = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)  # New field for location

    def __str__(self):
        return self.title
    
class MediaFile(models.Model):
    INCIDENT_TYPE_CHOICES = [
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video')
    ]

    incident_report = models.ForeignKey(IncidentReport, related_name='media_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/')
    file_type = models.CharField(max_length=10, choices=INCIDENT_TYPE_CHOICES, default='image')

    def __str__(self):
        return f"{self.file.name} ({self.file_type})"
    

