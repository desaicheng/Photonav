from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse, JsonResponse
from django.apps import apps
from Landmarks.functions import getPhotos
from commonFunctions.functions import fixString
from django.db import connection
from haversine import haversine, Unit
import json
import math

# photo = apps.get_model('Landmarks', 'photo')


class userInfo:
    def __init__(self):
        self.data = []
        self.userLatitude = "-75.2509766"
        self.userLongitude = "-0.071389"
        self.paginationNumber = 12
        self.sortType = 'Distance'
        self.radius = 1000000
        self.pageNum = 1


user = userInfo()


# get set of landmarks


def getLandmarks(request):
    if request.is_ajax():
        user.userLatitude = request.GET.get('latitude', None) if request.GET.get(
            'latitude', None) != 'skip' else user.userLatitude
        user.userLongitude = request.GET.get('longitude', None) if request.GET.get(
            'longitude', None) != 'skip' else user.userLongitude
        user.radius = float(request.GET.get('radius', 100000)) if int(request.GET.get(
            'radius', 100000)) != -1 else user.radius
        # page number
        page = int(request.GET.get('page', 1))
        start = (page-1)*user.paginationNumber
        end = page*user.paginationNumber
        maxDiff = user.radius/10
        queryStatement = 'SELECT * FROM Landmarks_landmark LEFT JOIN landmarks_frontPagePhotos ON Landmarks_landmark.neighborhood = landmarks_frontPagePhotos.landmark_id'
        user.data = getPhotos(queryStatement, user.userLatitude,
                              user.userLongitude, user.radius)
        sort(request)
        return HttpResponse(json.dumps(user.data[start:end]))
    else:
        raise Exception('Invaid Request')

# get information about a landmark


def getLandmarkInfo(request):
    if request.is_ajax():
        neighborhood = str(request.GET.get('neighborhood', None))
        neighborhood = fixString(neighborhood)
        queryStatement = 'SELECT * FROM Landmarks_photo WHERE landmark_id=\'{}\''.format(
            neighborhood)
        try:
            with connection.cursor() as cursor:
                cursor.execute(queryStatement)
                photos = cursor.fetchall()
        except:
            raise Exception('Could not get landmark info')
        photosInfo = []
        for photo in photos:
            distanceAway = haversine(
                (float(user.userLatitude), float(user.userLongitude)), (photo[4], photo[3]), unit="mi")
            curPhoto = {
                "imgSrc": "../static/images/{}/{}".format(photo[5].replace(" ", ""), photo[1]),
                "distanceAway": distanceAway,
                "directionsUrl": photo[2]
            }
            photosInfo.append(curPhoto)
        return HttpResponse(json.dumps(photosInfo))
    else:
        raise Exception('Invaid Request')


# change number of photos displayed on one page


def newPaginationNumber(request):
    if request.is_ajax():
        user.paginationNumber = int(request.GET.get('num', 12))
        # user.paginationNumber = 1
        numOfPages = math.ceil(len(user.data)/user.paginationNumber)
        ret = {
            "numOfPages": numOfPages,
        }
        return HttpResponse(json.dumps(ret))
    else:
        raise Exception('Invaid Request')

# sort landmarks by criteria


def sort(request):
    if user.sortType == 'Name':
        def Name(elem):
            return elem['neighborhood']
        user.data.sort(key=Name)
    elif user.sortType == 'Distance':
        def Distance(elem):
            return elem['distanceAway']
        user.data.sort(key=Distance)

# call sort function


def sortBy(request):
    if request.is_ajax():
        user.sortType = request.GET.get('type', None)
        sort(request)
        return HttpResponse(json.dumps(user.data[:user.paginationNumber]))
    else:
        raise Exception('Invaid Request')

# render home page


def home(request):
    return render(request, "home.html")
