from django.db import models
import paging

class QuerySetManager(models.Manager):
    use_for_related_fields = True
    def __init__(self, qs_class=models.query.QuerySet):
        self.queryset_class = qs_class
        super(QuerySetManager, self).__init__()

    def get_query_set(self):
        return self.queryset_class(self.model)

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)

class QuerySet(models.query.QuerySet):
    """Base QuerySet class for adding custom methods that are made
    available on both the manager and subsequent cloned QuerySets"""

    @classmethod
    def as_manager(cls, ManagerClass=QuerySetManager):
        return ManagerClass(cls)

class PaginatedQuerySet(QuerySet):

    def paginate(self, page_token=None, page_length=20):
        if page_length is None:
            page_length = 20
        page_length = int(page_length)
        padded_page_length = page_length + 1
        direction = None

        if page_length is None:
            page_length = 20
        if page_token is None:
            items = self.order_by('-id')[:padded_page_length]
        else:
            index, direction = paging.deconstruct_page_token(page_token)
            if direction == paging.Direction.Previous:
                filter_key = 'id__gt'
            else:
                filter_key = 'id__lt'
            filters = {filter_key: index}
            # Grab an extra one so that we can see if we are at the last page
            print filters
            items = self.filter(**filters).order_by('-id')[:padded_page_length]
        last_page = False
        if len(items) < padded_page_length:
            last_page = True
        
        #Now remove the extra item
        items = list(items[:page_length])
        if items:
            next_index = items[-1].id
            next_page = paging.construct_page_token(
                next_index, paging.Direction.Next)
            if direction == paging.Direction.Next and last_page:
                next_page = None

            prev_index = items[0].id
            prev_page = paging.construct_page_token(
                prev_index, paging.Direction.Previous)
            if direction == paging.Direction.Previous and last_page:
                prev_page = None
            return items, next_page, prev_page
        return items, None, None
        
