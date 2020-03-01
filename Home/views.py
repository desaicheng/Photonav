from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, JsonResponse
from django.apps import apps
from Landmarks.functions import getPhotos
import json

photo = apps.get_model('Landmarks', 'photo')
data = []


def getLatLon(request):
    global data
    if request.is_ajax():
        print('here')
        userLatitude = request.GET.get('latitude', None)
        userLongitude = request.GET.get('longitude', None)
        radius = float(request.GET.get('radius', 100000))
        maxDiff = radius/10
        queryStatement = 'SELECT * FROM Landmarks_photo WHERE ABS(longitude-{}) <= {} AND ABS(latitude-{}) <= {}'.format(
            userLongitude, maxDiff, userLatitude, maxDiff)
        data = getPhotos(queryStatement, userLatitude, userLongitude, radius)
        return HttpResponse(json.dumps(data))


def sortBy(request):
    sortType = request.GET.get('type', None)
    if sortType == 'Name':
        def Name(elem):
            return elem['neighborhood']
        data.sort(key=Name)
    elif sortType == 'Distance':
        def Distance(elem):
            return elem['distanceAway']
        data.sort(key=Distance)
    return HttpResponse(json.dumps(data))


def home(request):
    return render(request, "home.html")
