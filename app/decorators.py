from django.shortcuts import redirect
from .models import *


def admin_required(function):
    def wrap(*args, **kwargs):
        if args[0].user.role.role == Role.ADMIN:
            return function(*args, **kwargs)
        else:
            return redirect('login')
    return wrap
