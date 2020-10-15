from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse, JsonResponse
from django.apps import apps
from Landmarks.functions import getPhotos, getNames
from commonFunctions.functions import fixString, searchIndex
from django.db import connection
from haversine import haversine, Unit
from decouple import config
import json
import math
import requests


# change carousel images, assumes we are on first page of landmarks
def changeCarousel(request):
    if request.is_ajax():
        data = request.session['data']
        return HttpResponse(json.dumps({
            "landmarks": data[:4]
        }))
    else:
        raise Exception('Invaid Request')

# change the user longitude and latitude


def changeCity(request):
    if request.is_ajax():
        if 'init' in request.session:
            del request.session['init']
        city = request.POST.get('location', None)
        city = city.replace(" ", "")
        apiURL = 'https://www.mapquestapi.com/geocoding/v1/address?key={}&inFormat=kvp&outFormat=json&location={}&thumbMaps=false'.format(config('MAPQUEST_GEOCODING_API_KEY'),
                                                                                                                                          city)
        response = json.loads(requests.get(apiURL).text)
        resultCity = response['results'][0]["locations"][0]["adminArea5"]
        if resultCity == "":
            return HttpResponse(json.dumps({'found': False}))
        else:
            request.session['latitude'] = response['results'][0]["locations"][0]["latLng"]['lat']
            request.session['longitude'] = response['results'][0]["locations"][0]["latLng"]['lng']
            return HttpResponse(json.dumps({
                'found': True,
                'latitude': request.session['latitude'],
                'longitude': request.session['longitude']
            }
            ))
    else:
        raise Exception('Invaid Request')

# set user back to default


def defaultSession(request):
    request.session['data'] = []
    request.session['paginationNumber'] = 12
    request.session['latitude'] = "-75.2509766"
    request.session['longitude'] = "-0.071389"
    request.session['sortType'] = 'Distance'
    request.session['radius'] = 1000000
    request.session['isMobile'] = False
    if 'init' in request.session:
        del request.session['init']
    return

# get all Landmarks


def getLandmarkNames(request):
    if request.is_ajax():
        request.session['landmarks'] = request.GET.get('landmarks', None) if request.GET.get(
            'landmarks', None) != 'all' else -1
        if request.session['landmarks'] == -1:
            queryStatement = "SELECT * FROM landmarks_landmark"
            request.session['names'] = getNames(queryStatement)
        ret = {}
        ret['names'] = request.session['names']
        return HttpResponse(json.dumps(ret))
    else:
        raise Exception('Invaid Request')


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
        queryStatement = 'SELECT * FROM Landmarks_landmark LEFT JOIN landmarks_frontPagePhotos ON Landmarks_landmark.neighborhood = landmarks_frontPagePhotos.landmark_id'
        request.session['data'] = getPhotos(queryStatement, userLatitude,
                                            userLongitude, radius)
        data = request.session['data']
        ret = {}
        if 'init' not in request.session:
            request.session['init'] = True
            ret['10-miles'] = searchIndex(data, 10, 'distanceAway')
            ret['30-miles'] = searchIndex(data, 30, 'distanceAway')
            ret['60-miles'] = searchIndex(data, 60, 'distanceAway')
            ret['all'] = len(data)
        data = sort(request, data)
        ret['data'] = data[start:end]
        return HttpResponse(json.dumps(ret))
    else:
        raise Exception('Invaid Request')

# get information about a landmark


def getLandmarkInfo(request):
    if request.is_ajax():
        neighborhood = str(request.GET.get('neighborhood', None))
        neighborhood = fixString(neighborhood)
        queryStatement = 'SELECT * FROM Landmarks_photo WHERE landmark_id=\'{}\''.format(
            neighborhood)
        userLatitude = request.session['latitude']
        userLongitude = request.session['longitude']
        try:
            with connection.cursor() as cursor:
                cursor.execute(queryStatement)
                photos = cursor.fetchall()
        except:
            raise Exception('Could not get landmark info')
        photosInfo = []
        for photo in photos:
            distanceAway = haversine(
                (float(userLatitude), float(userLongitude)), (photo[4], photo[3]), unit="mi")
            curPhoto = {
                "imgSrc": "/images/{}/{}".format(photo[5].replace(" ", "").lower(), photo[1]),
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
        # request.session['paginationNumber'] = 4
        # paginationNumber = 4
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
        print(data)
        data = sort(request, data)
        paginationNumber = request.session['paginationNumber']
        return HttpResponse(json.dumps(data[:paginationNumber]))
        # return HttpResponse(json.dumps({}))
    else:
        raise Exception('Invaid Request')

# render home page


def home(request):
    return render(request, "home.html")

# create a new Landmark


def createLandmark(request):
    home(request)
    return HttpResponse({})
