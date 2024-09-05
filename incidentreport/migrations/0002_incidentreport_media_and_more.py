# Generated by Django 4.2.4 on 2024-09-04 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidentreport', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidentreport',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='incidentreport',
            name='case_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='incidentreport',
            name='public_share_level',
            field=models.CharField(blank=True, choices=[('public', 'Public'), ('community', 'Community')], max_length=20, null=True),
        ),
    ]
