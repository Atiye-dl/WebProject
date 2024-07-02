from django.shortcuts import render
from django.http import Http404

def is_manager(user):
    try:
        if not user.is_manager:
            raise Http404
        return True
    except:
        raise Http404
