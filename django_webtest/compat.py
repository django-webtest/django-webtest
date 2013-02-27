import sys

PY3 = sys.version_info[0] == 3

if PY3:
    def to_string(s):
        if isinstance(s, str):
            return s
        return str(s, 'latin1')

    from urllib import parse as urlparse

else:

    def to_string(s):
        return str(s)

    import urlparse

