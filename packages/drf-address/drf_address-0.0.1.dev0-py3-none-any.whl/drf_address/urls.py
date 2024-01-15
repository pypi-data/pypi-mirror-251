from django.contrib import admin
from django.urls import path, include
from .routers import r
from .views import CountryListAPIView

urlpatterns = [
    path('', include(r.urls)),
    path('address/list-countries/', CountryListAPIView.as_view(), name='ListCountries')
]