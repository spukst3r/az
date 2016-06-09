from az.loader import get_object
import sh


class BaseAdapter(object):
    def __init__(self, params):
        self._as = params.get('as')
        self.run = sh

        if not self._as:
            raise RuntimeError("Missing required parameter for bgp: as")

        self.init_adapter(params.get('config', {}))

    def init_adapter(self, cfg):
        pass

    def get_routed_ips(self):
        pass

    def route_ips(self, ips):
        pass

    def unroute_ips(self, ips):
        pass


def get_adapter(name):
    return get_object('az.bgp', name)
