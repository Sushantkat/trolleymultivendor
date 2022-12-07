from django.core.exceptions import PermissionDenied


def is_seller():
    def decorator(view_function):
        def wrap(request, *args, **kwargs):
            if request.user.is_seller:
                return view_function(request, *args, **kwargs)
            else:
                raise PermissionDenied

        return wrap

    return decorator


def is_customer():
    def decorator(view_function):
        def wrap(request, *args, **kwargs):
            if request.user.is_customer:
                return view_function(request, *args, **kwargs)
            else:
                raise PermissionDenied

        return wrap

    return decorator
