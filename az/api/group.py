from az.api import Api
from az.utils import ip_tuple


class Order(Api):
    path = 'group.php'
    mock_file = 'az/mocks/group.txt'

    def process(self, data):
        l = filter(None, map(lambda s: s.split(','), data.split('\n')))

        return set(ip_tuple(item) for sublist in l for item in filter(None, sublist))


def exports(**kwargs):
    return Order
