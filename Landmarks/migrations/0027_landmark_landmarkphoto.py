# Generated by Django 3.0.3 on 2020-03-02 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Landmarks', '0026_landmarkphoto'),
    ]

    operations = [
        migrations.AddField(
            model_name='landmark',
            name='landmarkPhoto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Landmarks.landmarkPhoto'),
        ),
    ]