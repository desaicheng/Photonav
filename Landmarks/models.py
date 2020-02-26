from django.db import models

# Create your models here.


class landmark(models.Model):
    neighborhood = models.CharField(max_length=100,
                                    primary_key=True)

    def __str__(self):
        return self.neighborhood


class photo(models.Model):
    imgSrc = models.ImageField(max_length=255)
    directionsUrl = models.URLField(max_length=255)
    longitude = models.FloatField(max_length=15, db_index=True)
    latitude = models.FloatField(max_length=15, db_index=True)
    landmark = models.ForeignKey(
        landmark, on_delete=models.CASCADE, null=True, blank=True)
