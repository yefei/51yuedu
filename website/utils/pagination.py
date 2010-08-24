'''
Created on 2009-12-20
$Id$
@author: Yefe
'''
import types 

DEFAULT_PRE_PAGE = 30
DEFAULT_AJAX_PRE_PAGE = 30
DEFAULT_AJAX_PRE_PAGE_MIN = 1
DEFAULT_AJAX_PRE_PAGE_MAX = 1000
DEFAULT_FIELD_NAME = 'page'
DEFAULT_WINDOW = 3


class Paginator(object):
    def __init__(self, object_list, page, per_page=DEFAULT_PRE_PAGE):
        from django.core.paginator import Paginator, InvalidPage, EmptyPage
        self.paginator = Paginator(object_list, per_page)
        
        if page == 'first':
            self.page = 1
        elif page == 'last':
            self.page = self.paginator.num_pages
        else:
            try:
                self.page = int(page)
                if self.page < 1:
                    self.page = 1
            except ValueError:
                self.page = 1
        
        try:
            self.page_obj = self.paginator.page(self.page)
        except (EmptyPage, InvalidPage):
            self.page = 1
            self.page_obj = self.paginator.page(1)
        
        self.count = self.paginator.count
        self.pages = self.paginator.num_pages
        self.object_list = self.page_obj.object_list
        

class TemplatePaginator(Paginator):
    def __init__(self, object_list, request, per_page=DEFAULT_PRE_PAGE, field_name=DEFAULT_FIELD_NAME):
        super(TemplatePaginator, self).__init__(object_list, request.GET.get(field_name, 0), per_page)
        self.request = request
        self.field_name = field_name
    
    def get_vars(self):
        if hasattr(self, '_get_vars_cached'):
            return self._get_vars_cached
        vars = self.request.GET.copy()
        if self.field_name in vars:
            del vars[self.field_name]
        if len(vars.keys()) > 0:
            self._get_vars_cached = "&%s" % vars.urlencode()
        else:
            self._get_vars_cached = ''
        return self._get_vars_cached
    
    def page_window_range(self, window=DEFAULT_WINDOW):
        page_range = self.paginator.page_range
        # First and last are simply the first *n* pages and the last *n* pages,
        # where *n* is the current window size.
        first = set(page_range[:window])
        last = set(page_range[-window:])
        # Now we look around our current page, making sure that we don't wrap
        # around.
        current_start = self.page_obj.number-1-window
        if current_start < 0:
            current_start = 0
        current_end = self.page_obj.number-1+window
        if current_end < 0:
            current_end = 0
        current = set(page_range[current_start:current_end])
        pages = []
        # If there's no overlap between the first set of pages and the current
        # set of pages, then there's a possible need for elusion.
        if len(first.intersection(current)) == 0:
            first_list = list(first)
            first_list.sort()
            second_list = list(current)
            second_list.sort()
            pages.extend(first_list)
            diff = second_list[0] - first_list[-1]
            # If there is a gap of two, between the last page of the first
            # set and the first page of the current set, then we're missing a
            # page.
            if diff == 2:
                pages.append(second_list[0] - 1)
            # If the difference is just one, then there's nothing to be done,
            # as the pages need no elusion and are correct.
            elif diff == 1:
                pass
            # Otherwise, there's a bigger gap which needs to be signaled for
            # elusion, by pushing a None value to the page list.
            else:
                pages.append(None)
            pages.extend(second_list)
        else:
            unioned = list(first.union(current))
            unioned.sort()
            pages.extend(unioned)
        # If there's no overlap between the current set of pages and the last
        # set of pages, then there's a possible need for elusion.
        if len(current.intersection(last)) == 0:
            second_list = list(last)
            second_list.sort()
            diff = second_list[0] - pages[-1]
            # If there is a gap of two, between the last page of the current
            # set and the first page of the last set, then we're missing a 
            # page.
            if diff == 2:
                pages.append(second_list[0] - 1)
            # If the difference is just one, then there's nothing to be done,
            # as the pages need no elusion and are correct.
            elif diff == 1:
                pass
            # Otherwise, there's a bigger gap which needs to be signaled for
            # elusion, by pushing a None value to the page list.
            else:
                pages.append(None)
            pages.extend(second_list)
        else:
            differenced = list(last.difference(current))
            differenced.sort()
            pages.extend(differenced)
        
        return pages

class TemplateRESTPaginator(Paginator):
    def __init__(self, object_list, reverse, reverse_args, page=1, per_page=DEFAULT_PRE_PAGE):
        super(TemplateRESTPaginator, self).__init__(object_list, page, per_page)
        self.reverse = reverse
        self.reverse_args = reverse_args
    
    def get_url(self, page=None):
        from django.core.urlresolvers import reverse
        if page is None:
            return reverse(self.reverse, args=self.reverse_args)
        else:
            return reverse(self.reverse, args=list(self.reverse_args)+[page])
    
    def page_window_range(self, window=DEFAULT_WINDOW):
        page_range = self.paginator.page_range
        # First and last are simply the first *n* pages and the last *n* pages,
        # where *n* is the current window size.
        first = set(page_range[:window])
        last = set(page_range[-window:])
        # Now we look around our current page, making sure that we don't wrap
        # around.
        current_start = self.page_obj.number-1-window
        if current_start < 0:
            current_start = 0
        current_end = self.page_obj.number-1+window
        if current_end < 0:
            current_end = 0
        current = set(page_range[current_start:current_end])
        pages = []
        # If there's no overlap between the first set of pages and the current
        # set of pages, then there's a possible need for elusion.
        if len(first.intersection(current)) == 0:
            first_list = list(first)
            first_list.sort()
            second_list = list(current)
            second_list.sort()
            pages.extend(first_list)
            diff = second_list[0] - first_list[-1]
            # If there is a gap of two, between the last page of the first
            # set and the first page of the current set, then we're missing a
            # page.
            if diff == 2:
                pages.append(second_list[0] - 1)
            # If the difference is just one, then there's nothing to be done,
            # as the pages need no elusion and are correct.
            elif diff == 1:
                pass
            # Otherwise, there's a bigger gap which needs to be signaled for
            # elusion, by pushing a None value to the page list.
            else:
                pages.append(None)
            pages.extend(second_list)
        else:
            unioned = list(first.union(current))
            unioned.sort()
            pages.extend(unioned)
        # If there's no overlap between the current set of pages and the last
        # set of pages, then there's a possible need for elusion.
        if len(current.intersection(last)) == 0:
            second_list = list(last)
            second_list.sort()
            diff = second_list[0] - pages[-1]
            # If there is a gap of two, between the last page of the current
            # set and the first page of the last set, then we're missing a 
            # page.
            if diff == 2:
                pages.append(second_list[0] - 1)
            # If the difference is just one, then there's nothing to be done,
            # as the pages need no elusion and are correct.
            elif diff == 1:
                pass
            # Otherwise, there's a bigger gap which needs to be signaled for
            # elusion, by pushing a None value to the page list.
            else:
                pages.append(None)
            pages.extend(second_list)
        else:
            differenced = list(last.difference(current))
            differenced.sort()
            pages.extend(differenced)
        
        return pages

class AjaxPaginator(Paginator):
    def __init__(self, object_list, request, data_repr=None, page_field_name='page', per_page_field_name='per_page'):
        try:
            per_page = int(request.REQUEST.get(per_page_field_name, DEFAULT_AJAX_PRE_PAGE))
            if per_page < DEFAULT_AJAX_PRE_PAGE_MIN or per_page > DEFAULT_AJAX_PRE_PAGE_MAX:
                per_page = DEFAULT_AJAX_PRE_PAGE
        except ValueError:
            per_page = DEFAULT_AJAX_PRE_PAGE
        super(AjaxPaginator, self).__init__(object_list, request.REQUEST.get(page_field_name, 0), per_page)
        self.data_repr = data_repr
    
    def _data_repr(self):
        t = type(self.data_repr)
        if t in (types.FunctionType, types.LambdaType):
            return [self.data_repr(o) for o in self.object_list]
        if t in (types.ListType, types.TupleType):
            return self.object_list.values(*self.data_repr)
        return self.object_list.values()
    
    def result(self):
        return {'total_counts':self.count,
                'total_pages':self.pages,
                'current_counts':len(self.object_list),
                'current_page':self.page,
                'per_page':self.paginator.per_page,
                'data':self._data_repr()}


