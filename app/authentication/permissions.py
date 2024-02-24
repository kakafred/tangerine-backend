from functools import wraps
from flask import abort
from flask_login import current_user


def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role != role:
                abort(403)
            return view_func(*args, **kwargs)
        return wrapper
    return decorator
