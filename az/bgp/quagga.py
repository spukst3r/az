import re
from shlex import quote

from az.bgp import BaseAdapter
from az.logger import getLogger
from az.utils import ip_valid, iterby, tuple_to_network


logger = getLogger(__name__)


def parse_quagga_output(output):
    network_re = re.compile(
        r'^[ \*][ \>]? *(([0-9]{1,3}\.){3}[0-9]{1,3})\/([0-9]{1,2}) *0\.0\.0\.0.*i$')
    res = []

    for line in output.split('\n'):
        m = network_re.match(line)
        mask_valid = True

        if m:
            ip, mask = m.group(1), m.group(3)

            try:
                mask = int(mask)
                assert(0 < mask <= 32)
            except:
                mask_valid = False

            if ip_valid(ip) and mask_valid:
                res.append((ip, mask))

    return res


def add_network(network):
    return 'network {}'.format(network)


def remove_network(network):
    return 'no {}'.format(add_network(network))


class Quagga(BaseAdapter):
    def get_routed_ips(self):
        logger.debug("Getting routed IPs")

        output = self.run.vtysh(c=quote('sh ip bgp'))

        return set(parse_quagga_output(output
                                       .stdout
                                       .decode('utf-8')))

    def route_ips(self, ips):
        for ip_set in iterby(ips, 50):
            logger.debug("Adding %d routes", len(ip_set))

            self.run.vtysh(c=quote('conf t\nrouter bgp {}\n{}'.format(
                self._as,
                '\n'.join(map(add_network, map(tuple_to_network, ip_set)))
            )))

    def unroute_ips(self, ips):
        for ip_set in iterby(ips, 50):
            logger.debug("Deleting %d routes", len(ip_set))

            self.run.vtysh(c=quote('conf t\nrouter bgp {}\n{}'.format(
                self._as,
                '\n'.join(map(remove_network, map(tuple_to_network, ip_set)))
            )))


def exports(**kwargs):
    return Quagga
