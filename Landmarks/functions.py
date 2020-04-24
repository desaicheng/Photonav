from .models import photo
from django.db import connection
from haversine import haversine, Unit
from commonFunctions.functions import searchIndex


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
            "imgSrc": "/images/{}/".format(spot[0].replace(" ", ""))+spot[2],
            "latitude": spot[4],
            "longitude": spot[3],
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
