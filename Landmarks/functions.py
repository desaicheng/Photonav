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
    if arr[r][key] > val:
        return r-1
    return r


def getPhotos(queryStatement, userLatitude, userLongitude, radius):
    with connection.cursor() as cursor:
        cursor.execute(queryStatement)
        data = cursor.fetchall()
    spots = []
    for spot in data:
        newObj = {
            "imgSrc": "../static/images/{}/".format(spot[0].replace(" ", ""))+spot[2],
            "latitude": spot[4],
            "longitude": spot[3],
            "neighborhood": spot[0]

        }
        newObj['distanceAway'] = haversine(
            (float(userLatitude), float(userLongitude)), (newObj['latitude'], newObj['longitude']), unit="mi")
        spots.append(newObj)
    print(spots)

    def distance(elem):
        return elem['distanceAway']
    spots.sort(key=distance)
    maxIndex = searchIndex(spots, radius, 'distanceAway')
    return spots[:maxIndex]
