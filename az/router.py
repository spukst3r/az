from az.logger import getLogger
from az.config import ConfigWrapper


logger = getLogger(__name__)


class Router(object):
    def __init__(self, config):
        config = ConfigWrapper(config)

        self.adapter = config.adapter
        self.api = config.api
        self.config = config

    def __call__(self):
        routed_ips = self.adapter.get_routed_ips()
        static_ips = self.config.static_ips
        api_ips = self.api.ip_list()

        to_delete = routed_ips - (static_ips | api_ips)
        to_add = (static_ips | api_ips) - routed_ips

        if to_delete:
            self.adapter.unroute_ips(to_delete)

        if to_add:
            self.adapter.route_ips(to_add)

        logger.info("Added %d routes, deleted %d routes", len(to_add), len(to_delete))
