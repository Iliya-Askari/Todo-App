from rest_framework.pagination import PageNumberPagination

class LargeResultsSetPagination(PageNumberPagination):
    '''
    Creating custom pagination for task lists
    '''
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10