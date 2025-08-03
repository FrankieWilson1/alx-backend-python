from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    A class that set a default page size of 20 and allows
    clients to request a different page size up to 100
    using a page_size query parameter.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
