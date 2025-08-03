from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    This custom pagination class sets the default page size for the resutl.
    A common use-case for pagination is to display the total count of items,
    which can be accessed via `page.paginator.count`.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
