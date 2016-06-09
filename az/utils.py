import socket
import functools
import struct

from az.logger import getLogger


logger = getLogger(__name__)


def ip_valid(ip):
    try:
        socket.inet_pton(socket.AF_INET, ip)
    except socket.error:
        return False

    return True


def ip_to_int(ip):
    _ipn = socket.inet_pton(socket.AF_INET, ip)

    return struct.unpack('!I', _ipn)[0]


def int_to_ip(ipn):
    return socket.inet_ntoa(struct.pack('!I', ipn))


def normalize_network(network):
    ipn = ip_to_int(network[0])
    mask = network[1]

    bin_mask = functools.reduce(lambda s, n: s + (1 << n),
                                range(0, mask), 0) << (32 - mask)

    return (int_to_ip(ipn & bin_mask), mask)


def collapse_networks(addresses, net_mask=24, threshold=10):
    int_addresses = []

    bin_mask = functools.reduce(lambda s, n: s + (1 << n),
                                range(0, net_mask), 0) << (32 - net_mask)

    for address, mask in addresses:
        try:
            ipn = ip_to_int(address)
        except socket.error:
            logger.error("Invalid IPv4 address: %s", address)
            continue

        int_addresses.append((ipn, mask))

    h = group(int_addresses, lambda n: n[0] & bin_mask)

    res = []

    for ipn in h:
        network = int_to_ip(ipn)
        ip_count = len(h[ipn])

        if ip_count > threshold:
            res.append((network, net_mask))
        else:
            for network in h[ipn]:
                ip = int_to_ip(network[0])
                res.append((ip, network[1]))

    return set(res)


def group(lst, func):
    res = {}

    for a in lst:
        h = func(a)

        if h in res:
            res[h].append(a)
        else:
            res[h] = [a]

    return res


def tuple_to_network(t):
    return '{}/{}'.format(t[0], t[1])


def ip_tuple(network):
    parsed = network.split('/')
    mask_valid = True

    def error():
        raise RuntimeError("Invalid network: {}".format(network))

    if len(parsed) == 2:
        ip, mask = parsed
    elif len(parsed) == 1:
        ip = parsed[0]
        mask = '32'
    else:
        error()

    try:
        mask = int(mask)
        assert(0 < mask <= 32)
    except:
        mask_valid = False

    if not (ip_valid and mask_valid):
        error()

    return normalize_network((ip, mask))


def iterby(iterator, count):
    it = iter(iterator)
    stop = False

    while True:
        res = []

        for i in range(count):
            try:
                res.append(next(it))
            except StopIteration:
                stop = True

        yield res

        if stop:
            next(it)
