from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse, JsonResponse
from django.apps import apps
from Landmarks.functions import getPhotos
from commonFunctions.functions import fixString
from django.db import connection
from haversine import haversine, Unit
import json
import math


# set user back to default


def defaultSession(request):
    request.session['data'] = []
    request.session['paginationNumber'] = 12
    request.session['latitude'] = "-75.2509766"
    request.session['longitude'] = "-0.071389"
    request.session['sortType'] = 'Distance'
    request.session['radius'] = 1000000
    request.session['isMobile'] = False
    return

# get set of landmarks


def getLandmarks(request):
    if request.is_ajax():
        request.session['latitude'] = request.GET.get('latitude', None) if request.GET.get(
            'latitude', None) != 'skip' else request.session['latitude']
        userLatitude = request.session['latitude']
        request.session['longitude'] = request.GET.get('longitude', None) if request.GET.get(
            'longitude', None) != 'skip' else request.session['longitude']
        userLongitude = request.session['longitude']
        request.session['radius'] = float(request.GET.get('radius', 100000)) if int(request.GET.get(
            'radius', 100000)) != -1 else request.session['radius']
        radius = request.session['radius']
        paginationNumber = request.session['paginationNumber']
        # page number
        page = int(request.GET.get('page', 1))
        start = (page-1)*paginationNumber
        end = page*paginationNumber
        maxDiff = radius/10
        queryStatement = 'SELECT * FROM Landmarks_landmark LEFT JOIN landmarks_frontPagePhotos ON Landmarks_landmark.neighborhood = landmarks_frontPagePhotos.landmark_id'
        request.session['data'] = getPhotos(queryStatement, userLatitude,
                                            userLongitude, radius)
        data = request.session['data']
        data = sort(request, data)
        return HttpResponse(json.dumps(data[start:end]))
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
        request.session['paginationNumber'] = int(request.GET.get('num', 12))
        paginationNumber = request.session['paginationNumber']
        data = request.session['data']
        numOfPages = math.ceil(len(data)/paginationNumber)
        ret = {
            "numOfPages": numOfPages
        }
        return HttpResponse(json.dumps(ret))
    else:
        raise Exception('Invaid Request')

# set to Desktop


def setDesktop(request):
    if request.is_ajax():
        defaultSession(request)
        print(request.session['isMobile'])
        return HttpResponse(json.dumps({}))
    else:
        raise Exception('Invaid Request')

# set to Mobile


def setMobile(request):
    if request.is_ajax():
        defaultSession(request)
        request.session['isMobile'] = True
        request.session['paginationNumber'] = 4
        return HttpResponse(json.dumps({}))
    else:
        raise Exception('Invaid Request')


# sort landmarks by criteria


def sort(request, data):
    sortType = request.session['sortType']
    if sortType == 'Name':
        def Name(elem):
            return elem['neighborhood']
        data.sort(key=Name)
    elif sortType == 'Distance':
        def Distance(elem):
            return elem['distanceAway']
        data.sort(key=Distance)
    return data

# call sort function


def sortBy(request):
    if request.is_ajax():
        request.session['sortType'] = request.GET.get('type', None)
        data = request.session['data']
        data = sort(request, data)
        print(data)
        paginationNumber = request.session['paginationNumber']
        return HttpResponse(json.dumps(data[:paginationNumber]))
        # return HttpResponse(json.dumps({}))
    else:
        raise Exception('Invaid Request')

# render home page


def home(request):
    return render(request, "home.html")
