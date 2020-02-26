from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
# import urllib3
# Create your views here.


# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip


# IP_URL = "http://ip-api.com/json/"


# def get_coords(ip):
#     url = IP_URL + ip
#     http = urllib3.PoolManager()
#     response = http.request('GET', url)
#     return response


def getLatLon(request):
    latitude = request.GET.get('latitude', None)
    longitude = request.GET.get('longitude', None)
    data = {
        "latitude": latitude,
        'longitude': longitude,
        't': 'fdsf'
    }
    return JsonResponse(data)


def home(request):
    # ip = get_client_ip(request)
    # ip = '74.118.212.2'
    # l = get_coords(ip)
    # print(l.status)
    # print(l.data.decode("utf-8"))
    return render(request, "home.html")
