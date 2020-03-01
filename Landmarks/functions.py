from .models import photo
from django.db import connection
from haversine import haversine, Unit


def searchIndex(arr, val, key):
    l = 0
    r = len(arr)-1
    while r-l > 1:
        m = (r+l)//2
        if arr[m][key] < val:
            l = m
        else:
            r = m
    return r


def getPhotos(queryStatement, userLatitude, userLongitude, radius):
    with connection.cursor() as cursor:
        cursor.execute(queryStatement)
        data = cursor.fetchall()
    spots = []
    for spot in data:
        ending = len(spot[1])-spot[1].rfind('.')
        newObj = {
            "directionsUrl": spot[2],
            "imgId": spot[0],
            "imgSrc": "../static/images/{}/".format(spot[5].replace(" ", ""))+spot[1][:28-ending]+spot[1][-ending:],
            "latitude": spot[4],
            "longitude": spot[3],
            "neighborhood": spot[5]

        }
        newObj['distanceAway'] = haversine(
            (float(userLatitude), float(userLongitude)), (newObj['latitude'], newObj['longitude']), unit="mi")
        spots.append(newObj)

    def distance(elem):
        return elem['distanceAway']
    spots.sort(key=distance)
    maxIndex = searchIndex(spots, radius, 'distanceAway')
    return spots[:maxIndex]
