

from urllib.parse import urlparse


def split_url_path(url):
    """Split "directory" segments in a URL path.
    """
    parsed = urlparse(url)

    return parsed.path.strip('/').split('/')


def try_or_none(f):
    """Wrap a class method call in a try block. If an error is raised, return
    None and log the exception.
    """
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            return None
    return wrapper
