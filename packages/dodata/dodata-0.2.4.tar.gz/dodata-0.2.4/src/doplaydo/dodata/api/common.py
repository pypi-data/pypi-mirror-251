"""Common utilities for the api portion of the sdk."""
import requests
from functools import partial
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .. import settings

__all__ = ["get", "post", "delete", "put"]


def session_with_backoff(
    max_retries: int = 5, backoff_factor: float = 0.05
) -> requests.Session:
    """Create requests with retries and backoff.

    Args:
        max_retries: Number of times to retry requests
        backoff_factor: each time a request fails, wait 0.05 * 2^()
    """
    session = requests.Session()
    retries = Retry(
        total=max_retries,
        read=max_retries,
        connect=max_retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.verify = settings.ssl_verify
    return session


session = session_with_backoff()

url = settings.dodata_url
auth = HTTPBasicAuth(settings.dodata_user, settings.dodata_password)

delete = partial(session.delete, auth=auth)
get = partial(session.get, auth=auth)
post = partial(session.post, auth=auth)
put = partial(session.put, auth=auth)
