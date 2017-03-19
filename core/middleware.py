from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


class AuthCheckerMiddleware(MiddlewareMixin):
    allowed_urls = [reverse('login'), reverse('core:registration')]

    def process_request(self, request):
        if not request.user.is_authenticated() and request.path not in self.allowed_urls:
            return HttpResponseRedirect(reverse('login'))
        else:
            return None
