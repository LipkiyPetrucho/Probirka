from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('api/catalog/', include('catalog.urls')),
    path('api/feedback/', include('feedback.urls')),
]
