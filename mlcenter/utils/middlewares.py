# create a middleware class that checks if user is authenticated and if not, redirects to login page
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.urls import resolve

class LoginRequiredMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_not_authenticated = not hasattr(request,'user') or not request.user.is_authenticated
        whitelisted_names = [
            'account_login',
            'account_signup',
            'account_logout',
            'account_reset_password',
            'account_reset_password_done',
            'account_reset_password_from_key',
            'account_reset_password_from_key_done',
            'account_confirm_email',
            'account_confirm_email_done',
        ]

        
        if user_not_authenticated and request.path_info.startswith('/api/') or request.path_info.startswith('/auth-token/'):
            response = self.get_response(request)
            return response
        
        if user_not_authenticated and resolve(request.path_info).url_name not in whitelisted_names:
            return HttpResponseRedirect(reverse_lazy('account_login'))
        
        response = self.get_response(request)
        return response