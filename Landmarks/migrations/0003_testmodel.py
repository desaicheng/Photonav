# Generated by Django 3.0.3 on 2020-02-25 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Landmarks', '0002_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='testModel',
            fields=[
                ('randomField', models.CharField(max_length=10, primary_key=True, serialize=False)),
            ],
        ),
    ]
