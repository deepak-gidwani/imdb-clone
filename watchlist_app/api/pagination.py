from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = 7
    page_size_query_params = 'size'
    max_page_size = 10

class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 5  # offset limit
    max_limit = 10  
    
class WatchListCPagination(CursorPagination):
    page_size = 5
    ordering = 'created'  