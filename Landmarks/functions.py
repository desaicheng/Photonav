from .models import photo
from django.db import connection
from haversine import haversine, Unit


def getPhotos(queryStatement, userLatitude, userLongitude):
    with connection.cursor() as cursor:
        cursor.execute(queryStatement)
        data = cursor.fetchall()
    spots = []
    for spot in data:
        newObj = {
            "directionsUrl": spot[2],
            "imgId": spot[0],
            "imgSrc": "../static/images/{}/".format(spot[5].replace(" ", ""))+spot[1][:24]+'.jpg',
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
    return spots
