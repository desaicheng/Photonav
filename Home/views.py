from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, JsonResponse
from django.apps import apps
from Landmarks.functions import getPhotos
import json

photo = apps.get_model('Landmarks', 'photo')


def getLatLon(request):
    if request.is_ajax():
        userLatitude = request.GET.get('latitude', None)
        userLongitude = request.GET.get('longitude', None)
        radius = 3000
        maxDiff = radius/10
        queryStatement = 'SELECT * FROM Landmarks_photo WHERE ABS(longitude-{}) <= {} AND ABS(latitude-{}) <= {}'.format(
            userLongitude, maxDiff, userLatitude, maxDiff)
        data = getPhotos(queryStatement, userLatitude, userLongitude)
        return HttpResponse(json.dumps(data))


def home(request):
    return render(request, "home.html")
