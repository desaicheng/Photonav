from django.urls import path
from .views import home, getLandmarks, sortBy

urlpatterns = [
    path('', home, name="home"),
    path('ajax/getLandmarks', getLandmarks, name="getLandmarks"),
    path('ajax/sortBy', sortBy, name="sortBy"),
]
