from django.urls import path
from .views import home, getLatLon, sortBy

urlpatterns = [
    path('', home, name="home"),
    path('ajax/getLatLon', getLatLon, name="getLatLon"),
    path('ajax/sortBy', sortBy, name="sortBy"),
]
