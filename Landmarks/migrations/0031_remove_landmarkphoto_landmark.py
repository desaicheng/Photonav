# Generated by Django 3.0.3 on 2020-03-02 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Landmarks', '0030_auto_20200302_1844'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='landmarkphoto',
            name='landmark',
        ),
    ]