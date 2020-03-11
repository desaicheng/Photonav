from django.urls import path
from .views import errorPage

urlpatterns = [
    path('', errorPage, name="errorPage"),
]
