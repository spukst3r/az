import yaml

from az import constants, bgp, api
from az.utils import ip_tuple


def singleton_config(f):
    registry = {}

    def wrapper(path):
        if path not in registry:
            registry[path] = f(path)

        return registry[path]

    return wrapper


@singleton_config
def get_config(path):
    with open(path) as cfg:
        return yaml.load(cfg)


class ConfigWrapper(object):
    def __init__(self, config):
        self.config = config

    @property
    def _az(self):
        return self.config.get('az', {})

    @property
    def _bgp(self):
        return self.config.get('bgp', {})

    @property
    def adapter(self):
        name = self._bgp.get('adapter', constants.DEFAULT_ADAPTER)
        Adapter = bgp.get_adapter(name)

        return Adapter(self._bgp)

    @property
    def static_ips(self):
        return set(map(ip_tuple, self._az.get('static', [])))

    @property
    def api_base_url(self):
        return self._az.get('base_url', constants.DEFAULT_BASE_URL)

    @property
    def api(self):
        method = self._az.get('method', constants.DEFAULT_METHOD)

        return api.get_api(method)(self.api_base_url)
