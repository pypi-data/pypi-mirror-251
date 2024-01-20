import os
import logging
from io import StringIO

from scrapy import signals
from scrapy.exceptions import NotConfigured

from .utils import get_client, get_release


class Errors(object):
    def __init__(self, dsn=None, **kwargs):
        self.client = get_client(dsn, **kwargs)  # Initialize Sentry SDK

    @classmethod
    def from_crawler(cls, crawler, dsn=None):
        release = crawler.settings.get("RELEASE", get_release(crawler))

        dsn = os.environ.get("SENTRY_DSN", crawler.settings.get("SENTRY_DSN", None))
        if dsn is None:
            raise NotConfigured("No SENTRY_DSN configured")
        extension = cls(dsn=dsn, release=release)
        crawler.signals.connect(extension.spider_error, signal=signals.spider_error)
        return extension

    def spider_error(self, failure):
        traceback = StringIO()
        failure.printTraceback(file=traceback)
        self.client.capture_exception(failure.value)
        logging.log(logging.WARNING, "Sentry Exception captured")

