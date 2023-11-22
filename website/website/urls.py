from django.contrib import admin
from django.urls import (
    path,
    include
)

# Inclui urls do app
urlpatterns = [
    path('', include('main.urls')),
    path("admin/", admin.site.urls),
]
