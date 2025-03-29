from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class RedirectIfLoggedInMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.path == '/accounts/login/':
            return redirect('/')