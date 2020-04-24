from django.urls import path
from .views import createLandmark
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('createlandmark', createLandmark,
         name="createLandmark"),
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
