# Generated by Django 3.0.3 on 2020-03-02 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Landmarks', '0012_delete_testmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='landmarkPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imgSrc', models.ImageField(default='../static/images/Extras/notFound.jpg', max_length=255, upload_to='')),
                ('longitude', models.FloatField(db_index=True, default='-0.071389', max_length=15)),
                ('latitude', models.FloatField(db_index=True, default='-75.2509766', max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='landmark',
            name='landmarkPhoto',
            field=models.ForeignKey(blank=True, default='-1', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='Landmarks.landmarkPhoto'),
        ),
    ]