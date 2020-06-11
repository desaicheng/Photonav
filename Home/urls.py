from django.urls import path
from .views import home, getLandmarks, sortBy, getLandmarkInfo, newPaginationNumber, setMobile, setDesktop, changeCity, createLandmark, changeCarousel

urlpatterns = [
    path('', home, name="home"),
    path('ajax/changeCity', changeCity, name="changeCity"),
    path('ajax/getLandmarks', getLandmarks, name="getLandmarks"),
    path('ajax/sortBy', sortBy, name="sortBy"),
    path('ajax/getLandmarkInfo', getLandmarkInfo, name="getLandmarkInfo"),
    path('ajax/newPaginationNumber', newPaginationNumber,
         name="newPaginationNumber"),
    path('ajax/setMobile', setMobile,
         name="setMobile"),
    path('ajax/setDesktop', setDesktop,
         name="setDesktop"),
    path('createLandmark', createLandmark,
         name="createLandmark"),
    path('ajax/changeCarousel', changeCarousel,
         name="changeCarousel"),
]
