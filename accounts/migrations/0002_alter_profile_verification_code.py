# Generated by Django 4.2.4 on 2024-09-05 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='verification_code',
            field=models.CharField(default='000000', max_length=6),
        ),
    ]
