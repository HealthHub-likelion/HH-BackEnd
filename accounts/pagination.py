from rest_framework.pagination import PageNumberPagination

class RankingPagination(PageNumberPagination):
    page_size = 50