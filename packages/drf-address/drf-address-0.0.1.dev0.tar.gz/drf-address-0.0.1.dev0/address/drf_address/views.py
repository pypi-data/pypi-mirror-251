from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Country
from .serializers import CountrySerializer
from .pagination import CountriesPagination

class CountryListAPIView(ListAPIView):
    """
    API View to return a list of all availaible countries for use on frontend.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = CountriesPagination

