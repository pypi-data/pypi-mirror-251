from rest_framework.pagination import LimitOffsetPagination

class CountriesPagination(LimitOffsetPagination):
    default_limit = 50