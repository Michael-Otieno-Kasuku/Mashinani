from django.contrib import admin
from django.urls import include, path

urlpatterns=[
    path("bursary/mashinani/", include("mashinani.urls")),
    path("bursary/mashinani/admin/",admin.site.urls),
]
