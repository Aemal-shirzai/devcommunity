from django.shortcuts import render, redirect
def must_not_login(fallback_url):
    def decorator(function):
        def wrapper(*args, **kwargs):
            request = args[0]
            if request.user.is_authenticated:
                return redirect(fallback_url)
            return function(*args, **kwargs)
        return wrapper
    return decorator