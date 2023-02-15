import re
from django.conf import settings
from django.contrib.auth.decorators import login_required

# for registering a class as middleware you at least __init__() and __call__()
# for this case we additionally need process_view() which will be automatically called by Django before rendering a view/template

class RequireLoginMiddleware(object):
    
    # need for one time initialization, here response is a function which will be called to get response from view/template
    def __init__(self, response):
        self.get_response = response
        self.required = tuple(re.compile(url) for url in settings.AUTH_URLS)
        self.exceptions = tuple(re.compile(url)for url in settings.NO_AUTH_URLS)

    def __call__(self, request):
        # //any code written here will be called before requesting response
        response = self.get_response(request)
        # //any code written here will be called after response
        return response

    # //this is called before requesting response
    def process_view(self, request, view_func, view_args, view_kwargs):
        # //if authenticated return no exception
        if request.user.is_authenticated:
            return None
        # //if found in allowed exceptional urls return no exception
        for url in self.exceptions:
            if url.match(request.path):
                return None
        # //return login_required()
        for url in self.required:
            if url.match(request.path):
                return login_required(view_func)(request, *view_args, **view_kwargs)
        # //default case, no exception
        return None