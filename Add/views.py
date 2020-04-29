from django.shortcuts import render, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.db import connection
import os
import boto3
from commonFunctions.functions import fixString
# Create your views here.

# tries to add new landmark to landmarks_landmark
# requires: landmark name or something that contains it
# throws exception if unable to insert


def addTolandmarks_landmark(landmarkName):
    fixedLandmarkName = landmarkName.replace(" ", "").lower()
    queryStatement = 'INSERT INTO landmarks_landmark (neighborhood,photoIndex) VALUES (\'{}\',0)'.format(
        fixString(landmarkName))
    try:
        with connection.cursor() as cursor:
            cursor.execute(queryStatement)
    except:
        raise Exception('Could not insert into landmarks_landmark')
    return

# uploads a photo to S3
# requires: request, photoIndex
# throws exception if unable to upload


def uploadPhotoToS3(request, photoIndex):
    landmarkImage = request.FILES['landmarkImage']
    landmarkName = request.POST['landmarkName']
    fixedLandmarkName = landmarkName.replace(" ", "").lower()
    session = boto3.Session(
        aws_access_key_id='AKIAR4BPJNOQKTGBSEGQ',
        aws_secret_access_key='y1PR1oIVk4yVXfyMwEl1pThgC3ZGpZDVVo4oKXiy'
    )
    s3 = session.resource('s3')
    s3.Bucket('photonav').put_object(Key='images/{}/{}_{}.jpg'.format(fixedLandmarkName, fixedLandmarkName, photoIndex),
                                     Body=landmarkImage)

# updates a landmark's photo index
# requires: landmark name, new photo index
# throws exception if unable to update


def updatePhotoIndex(landmarkName, photoIndex):
    fixedLandmarkName = fixString(landmarkName.replace(' ', '').lower())
    queryStatement = 'UPDATE landmarks_landmark SET photoIndex = {} WHERE LOWER(REPLACE(neighborhood,\' \',\'\')) = \'{}\''.format(
        photoIndex, fixedLandmarkName)
    print(queryStatement)
    try:
        with connection.cursor() as cursor:
            cursor.execute(queryStatement)
        return
    except:
        raise Exception('Could not update landmarks_landmark')

# gets the current photo index of a landmark
# requires: landmark name
# throws exception if unable to query


def getPhotoIndex(landmarkName):
    fixedLandmarkName = fixString(landmarkName.replace(' ', '').lower())
    queryStatement = 'SELECT * FROM landmarks_landmark WHERE LOWER(REPLACE(neighborhood,\' \',\'\')) = \'{}\''.format(
        fixedLandmarkName)
    try:
        with connection.cursor() as cursor:
            cursor.execute(queryStatement)
            photoIndex = cursor.fetchall()
            if len(photoIndex) == 0:
                photoIndex = 0
            else:
                photoIndex = photoIndex[0][1]
            return photoIndex
    except:
        raise Exception('Could not query landmarks_landmark')

# adds to landmarks_frontpagephotos, photoIndex is 1
# requires request
# throws exception is unable to insert


def addTolandmarks_frontpagephotos(request):
    landmarkLatitude = request.POST['landmarkLatitude']
    landmarkLongitude = request.POST['landmarkLongitude']
    landmarkName = request.POST['landmarkName']
    fixedLandmarkName = fixString(landmarkName.replace(' ', '').lower())
    imgSrc = fixedLandmarkName+'_1.jpg'
    queryStatement = 'INSERT INTO landmarks_frontpagephotos (imgSrc,longitude,latitude,landmark_id) VALUES (\'{}\',\'{}\',\'{}\',\'{}\')'.format(
        imgSrc, landmarkLongitude, landmarkLatitude, fixString(landmarkName))
    try:
        with connection.cursor() as cursor:
            cursor.execute(queryStatement)
        return
    except:
        raise Exception('Could not add to landmarks_frontpagephotos')

# tries to add new photo to landmarks_photo, updates photo Index in landmarks_landmark
# requires: request
# throws exception if unable to insert


def addTolandmarks_photo(request):
    landmarkLatitude = request.POST['landmarkLatitude']
    landmarkLongitude = request.POST['landmarkLongitude']
    landmarkName = request.POST['landmarkName']
    fixedLandmarkName = fixString(landmarkName.replace(' ', '').lower())
    photoIndex = getPhotoIndex(landmarkName) + 1
    updatePhotoIndex(landmarkName, photoIndex)
    directionsUrl = 'https://www.google.com/maps/dir/?api=1&destination={},{}'.format(
        landmarkLatitude, landmarkLongitude)
    imgSrc = fixedLandmarkName+'_{}.jpg'.format(photoIndex)
    queryStatement = 'INSERT INTO landmarks_photo (imgSrc,directionsUrl,longitude,latitude,landmark_id) VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'.format(
        imgSrc, directionsUrl, landmarkLongitude, landmarkLatitude, fixString(landmarkName))
    print(queryStatement)
    try:
        with connection.cursor() as cursor:
            cursor.execute(queryStatement)
        return
    except:
        raise Exception('Could not add to landmarks_photo')

# check if landmark already exists in database
# requires: a string with the name of a landmark
# returns: True if landmark already exists, otherwise returns False


def checkLandmarkExists(landmarkName):
    fixedLandmarkName = fixString(landmarkName.replace(' ', '').lower())
    queryStatement = 'SELECT * FROM landmarks_landmark WHERE LOWER(REPLACE(neighborhood,\' \',\'\')) = \'{}\''.format(
        fixedLandmarkName)
    try:
        with connection.cursor() as cursor:
            cursor.execute(queryStatement)
            landmark = cursor.fetchall()
            if len(landmark) > 0:
                print('landmark found')
                return True
            else:
                return False
    except:
        raise Exception('Could not check if landmark exists')


# create a new Landmark and save relevant info

def createLandmark(request):
    landmarkImage = request.FILES['landmarkImage']
    landmarkName = request.POST['landmarkName']
    if checkLandmarkExists(landmarkName):
        return HttpResponse({'response': 'landmark already exists'})
    else:
        print(' ')
        addTolandmarks_landmark(landmarkName)
        addTolandmarks_photo(request)
        addTolandmarks_frontpagephotos(request)
        uploadPhotoToS3(request, 1)
    #     addTolandmarks_landmark(landmarkName)
    # fixedLandmarkName = landmarkName.replace(" ", "").lower()
    # session = boto3.Session(
    #     aws_access_key_id='AKIAR4BPJNOQKTGBSEGQ',
    #     aws_secret_access_key='y1PR1oIVk4yVXfyMwEl1pThgC3ZGpZDVVo4oKXiy'
    # )
    # s3 = session.resource('s3')
    # s3.Bucket('photonav').put_object(Key='images/{}/{}_1.jpg'.format(fixedLandmarkName, fixedLandmarkName),
    #                                  Body=landmarkImage)
    return HttpResponse({'response': 'landmark successfully added'})
