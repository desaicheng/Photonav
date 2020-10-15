from .models import photo
from django.db import connection
from haversine import haversine, Unit
from commonFunctions.functions import searchIndex

# get all landmark names


def getNames(queryStatement):
    try:
        with connection.cursor() as cursor:
            cursor.execute(queryStatement)
            data = cursor.fetchall()
    except:
        raise Exception('Could not get Names')
    names = []
    for spot in data:
        names.append(spot[0])
    return names


def getPhotos(queryStatement, userLatitude, userLongitude, radius):
    try:
        with connection.cursor() as cursor:
            cursor.execute(queryStatement)
            data = cursor.fetchall()
    except:
        raise Exception('Could not get Photos')
    spots = []
    for spot in data:
        newObj = {
            "imgSrc": "/images/{}/".format(spot[0].replace(" ", "").lower())+spot[3],
            "latitude": spot[5],
            "longitude": spot[4],
            "neighborhood": spot[0]

        }
        newObj['distanceAway'] = haversine(
            (float(userLatitude), float(userLongitude)), (newObj['latitude'], newObj['longitude']), unit="mi")
        spots.append(newObj)
    if len(spots) == 0:
        return spots

    def distance(elem):
        return elem['distanceAway']
    spots.sort(key=distance)
    maxIndex = searchIndex(spots, radius, 'distanceAway')
    return spots[:maxIndex]
