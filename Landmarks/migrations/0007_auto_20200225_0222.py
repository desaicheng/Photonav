# Generated by Django 3.0.3 on 2020-02-25 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Landmarks', '0006_testmodel_newfields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testmodel',
            name='newFields',
            field=models.IntegerField(),
        ),
    ]
