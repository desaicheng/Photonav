from django.db import models
from s3direct.fields import S3DirectField
# Create your models here.


class photo(models.Model):
    img = S3DirectField(dest='primary_destination', blank=True)
