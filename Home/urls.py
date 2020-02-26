from django.urls import path
from .views import home, getLatLon

urlpatterns = [
    path('', home, name="home"),
    path('ajax/getLatLon', getLatLon, name="getLatLon"),
]
