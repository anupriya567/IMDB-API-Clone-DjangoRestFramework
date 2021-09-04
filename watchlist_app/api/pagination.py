from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class WatchListPagination(PageNumberPagination):
    page_size = 4
    page_query_param = 'pg'
    page_size_query_param = 'size' # power given to client what page size you want
    max_page_size = 10
    # last_page_strings = 'end'


# by default sorted from latest to prev acc. to created timestamp
# but we can modify it using ordering filter
class WatchListCPagination(CursorPagination):
    page_size = 4
    ordering = 'title'

    





