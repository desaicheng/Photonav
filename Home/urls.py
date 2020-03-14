from django.urls import path
from .views import home, getLandmarks, sortBy, getLandmarkInfo, newPaginationNumber

urlpatterns = [
    path('', home, name="home"),
    path('ajax/getLandmarks', getLandmarks, name="getLandmarks"),
    path('ajax/sortBy', sortBy, name="sortBy"),
    path('ajax/getLandmarkInfo', getLandmarkInfo, name="getLandmarkInfo"),
    path('ajax/newPaginationNumber', newPaginationNumber,
         name="newPaginationNumber"),
]
