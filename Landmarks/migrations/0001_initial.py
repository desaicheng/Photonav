# Generated by Django 3.0.3 on 2020-02-24 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='landmark',
            fields=[
                ('neighborhood', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
    ]
