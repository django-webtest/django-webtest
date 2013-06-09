import sys
import urllib

PY3 = sys.version_info[0] == 3

if PY3:
    from urllib import parse as urlparse

    def to_string(s):
        if isinstance(s, str):
            return s
        return str(s, 'latin1')

    def to_wsgi_safe_string(s):
        return urlparse.quote(to_string(s))

    def from_wsgi_safe_string(s):
        return urlparse.unquote(s)

else:
    import urlparse

    def to_string(s):
        return str(s)

    def to_wsgi_safe_string(s):
        return to_string(urllib.quote(s.encode('utf8')))

    def from_wsgi_safe_string(s):
        return urllib.unquote(s).decode('utf8')



