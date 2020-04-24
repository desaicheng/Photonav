from django.shortcuts import render, HttpResponse
from .forms import newLandmark
from django.core.files.storage import FileSystemStorage
import os
from .models import photo
from .forms import ImageUpload
# Create your views here.


# create a new Landmark and save relevant info


# def createLandmark(request):
#     if request.method == 'POST':
#         image = request.FILES['landmarkImage']
#         landmarkName = request.POST['landmarkName']
#         landmarkLatitude = request.POST['landmarkLatitude']
#         landmarkLongitude = request.POST['landmarkLongitude']
#         fs = FileSystemStorage(
#             location="staticfiles/{}/".format(landmarkName.replace(" ", "")))
#         image.name = 'test.png'
#         new_dir_path = os.path.join(
#             'staticfiles', "{}".format(landmarkName.replace(" ", "")))
#         os.mkdir(new_dir_path)
#         filename = fs.save(image.name, image)
#         uploaded_file_url = fs.url(filename)
#         print(landmarkName, 'fdsfs', image.name)
#         return HttpResponse({})
#     else:
#         raise Exception('Invaid Request')

def createLandmark(request):
    images = photo.objects.all()
    if request.method == 'POST':
        form = ImageUpload(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('portfolio')
    else:
        form = ImageUpload()
    return HttpResponse({})
