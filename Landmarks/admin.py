from django.contrib import admin
from .models import landmark, photo, frontPagePhotos
# Register your models here.
admin.site.register(landmark)
admin.site.register(photo)
admin.site.register(frontPagePhotos)
