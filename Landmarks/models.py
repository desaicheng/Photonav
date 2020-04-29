from django.db import models

# Create your models here.

# All landmarks and their current photo index


class landmark(models.Model):
    neighborhood = models.CharField(max_length=100,
                                    primary_key=True)
    photoIndex = models.IntegerField(max_length=17, null=True, blank=True)

    def __str__(self):
        return self.neighborhood

# photos to be displayed on carousel of a landmark


class frontPagePhotos(models.Model):
    imgSrc = models.ImageField(
        max_length=255, default="../static/images/Extras/notFound.jpg")
    longitude = models.FloatField(
        max_length=15, db_index=True, default="-0.071389")
    latitude = models.FloatField(
        max_length=15, db_index=True, default="-75.2509766")
    landmark = models.ForeignKey(
        landmark, on_delete=models.CASCADE, null=True, blank=True)
    directionsUrl = models.CharField(max_length=255, default=None)

    def __str__(self):
        return self.landmark.neighborhood

# All photos


class photo(models.Model):
    imgSrc = models.ImageField(max_length=255)
    directionsUrl = models.URLField(max_length=255)
    longitude = models.FloatField(
        max_length=15, db_index=True, default="-0.071389")
    latitude = models.FloatField(
        max_length=15, db_index=True, default="-75.2509766")
    landmark = models.ForeignKey(
        landmark, on_delete=models.CASCADE, null=True, blank=True)
