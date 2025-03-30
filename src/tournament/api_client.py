import logging

import requests
from django.core.cache import cache

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url=""):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        cache_value = cache.get(url)
        if cache_value:
            logger.debug("Fetching %s from cache.", url)
            return cache_value
        response = self.session.get(url, params=params)
        logger.debug("Fetching %s from the web.", url)
        response.raise_for_status()
        response = response.json()
        cache.set(url, response)
        return response

    def close(self):
        self.session.close()

    def __enter__(self):
        """Enter the runtime context (used for 'with' statement)."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context, ensuring the session is closed."""
        self.close()
