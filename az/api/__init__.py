import requests
import urllib

from az.logger import getLogger
from az.loader import get_object

logger = getLogger(__name__)


def wrap_read_exception(msg, default=None):
    def args(f):
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except:
                logger.exception("%s", msg)

                return default

        return wrapper

    return args


class Api(object):
    path = ''
    mock_file = ''

    def __init__(self, base_url, mock=False):
        self.base_url = base_url
        self.mock = mock

    @property
    def api_url(self):
        return urllib.parse.urljoin(self.base_url, self.path)

    def ip_list(self):
        @wrap_read_exception("Mock file reading failed", '')
        def read_mock():
            logger.debug("URL would be '%s'", self.api_url)

            with open(self.mock_file) as mf:
                return mf.read()

        @wrap_read_exception("API call failed", '')
        def call_api():
            return requests.get(self.api_url).text

        if self.mock:
            reader = read_mock
        else:
            reader = call_api

        try:
            return self.process(reader())
        except:
            logger.exception("Processing data failed")

    def process(self, data):
        raise NotImplemented("This method should be overriden by subclasses")


def get_api(method):
    return get_object('az.api', method)
