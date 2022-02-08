from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect

def business_required(function):
    def _function(request, *args, **kwargs):
        if request.user.account_type=="staff" or request.user.is_superuser:
            return function(request, *args, **kwargs)
        messages.error(request, 'You do not have business staff access')
        return redirect("login")
    return _function
