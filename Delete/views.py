from django.shortcuts import render
from commonFunctions.functions import fixString
from django.db import connection

# Create your views here.

# tries to delete a landmark to landmarks_landmark
# requires: landmark name
# throws exception if unable to delete


def deleteFromlandmarks_landmark(landmarkName):
    queryStatement = 'DELETE FROM landmarks_landmark WHERE neighborhood = \'{}\''.format(
        fixString(landmarkName))
    try:
        with connection.cursor() as cursor:
            cursor.execute(queryStatement)
    except:
        raise Exception('Could delete landmark from landmarks_landmark')
    return

# delete landmark from landmarks_frontpagephotos
# requires landmark name
# throws exception is unable to delete


def deleteFromlandmarks_frontpagephotos(landmarkName):
    queryStatement = 'DELETE FROM landmarks_frontpagephotos WHERE landmark_id = \'{}\''.format(
        fixString(landmarkName))
    try:
        with connection.cursor() as cursor:
            cursor.execute(queryStatement)
        return
    except:
        raise Exception(
            'Could not delete landmark from landmarks_frontpagephotos')

# tries delete all photos of a landmark from landmarks_photo
# requires: landmark Name
# throws exception if unable to delete


def addTolandmarks_photo(landmarkName):
    queryStatement = 'DELETE FROM landmarks_photo WHERE landmark_id = \'{}\''.format(
        fixString(landmarkName))
    try:
        with connection.cursor() as cursor:
            cursor.execute(queryStatement)
        return
    except:
        raise Exception('Could not add to landmarks_photo')


# tries to delete landmark from all database tables
# requires landmark Name


def deleteLandmark(landmarkName):
    deleteFromlandmarks_landmark(landmarkName)
    deleteFromlandmarks_frontpagephotos(landmarkName)
    addTolandmarks_photo(landmarkName)
