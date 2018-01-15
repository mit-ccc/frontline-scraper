

from urllib.parse import urlparse


def split_url_path(url):
    """Split "directory" segments in a URL path.
    """
    parsed = urlparse(url)

    return parsed.path.strip('/').split('/')
