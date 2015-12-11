from django_webtest.compat import to_wsgi_safe_string


def _get_username(user):
    """
    Return user's username. ``user`` can be standard Django User
    instance, a custom user model or just an username (as string).
    """
    if hasattr(user, 'get_username'):  # custom user, django 1.5+
        return user.get_username()
    elif hasattr(user, 'username'):    # standard User
        return user.username
    else:                              # assume user is just an username
        return user


def update_environ(environ, user):
    """
    Update environment ``environ`` to include ```user```
    """
    if user:
        environ = environ or {}
        username = _get_username(user)
        environ['WEBTEST_USER'] = to_wsgi_safe_string(username)
    return environ
