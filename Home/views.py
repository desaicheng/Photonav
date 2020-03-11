from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, JsonResponse
from django.apps import apps
from Landmarks.functions import getPhotos
from commonFunctions.functions import fixString
from django.db import connection
from haversine import haversine, Unit
import json

# photo = apps.get_model('Landmarks', 'photo')
data = []
userLatitude = "-75.2509766"
userLongitude = "-0.071389"


def errorPage(request):
    return render(request, "errorPage.html")


def getLandmarks(request):
    global data
    global userLatitude
    global userLongitude
    if request.is_ajax():
        userLatitude = request.GET.get('latitude', None)
        userLongitude = request.GET.get('longitude', None)
        radius = float(request.GET.get('radius', 100000))
        maxDiff = radius/10
        queryStatement = 'SELECT * FROM Landmarks_landmark LEFT JOIN landmarks_frontPagePhotos ON Landmarks_landmark.neighborhood = landmarks_frontPagePhotos.landmark_id'
        data = getPhotos(queryStatement, userLatitude, userLongitude, radius)
        return HttpResponse(json.dumps(data))
    else:
        raise Exception('Invaid Request')


def getLandmarkInfo(request):
    if request.is_ajax():
        neighborhood = str(request.GET.get('neighborhood', None))
        neighborhood = fixString(neighborhood)
        queryStatement = 'SELECT * FROM Landmarks_photo WHERE landmark_id=\'{}\''.format(
            neighborhood)
        with connection.cursor() as cursor:
            cursor.execute(queryStatement)
            photos = cursor.fetchall()
        photosInfo = []
        for photo in photos:
            distanceAway = haversine(
                (float(userLatitude), float(userLongitude)), (photo[4], photo[3]), unit="mi")
            curPhoto = {
                "imgSrc": "../static/images/{}/{}".format(photo[5].replace(" ", ""), photo[1]),
                "distanceAway": distanceAway,
                "directionsUrl": photo[2]
            }
            photosInfo.append(curPhoto)
        return HttpResponse(json.dumps(photosInfo))
    else:
        raise Exception('Invaid Request')


def sortBy(request):
    if request.is_ajax():
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
    else:
        raise Exception('Invaid Request')


def home(request):
    return render(request, "home.html")
