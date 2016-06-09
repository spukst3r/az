import logging
from logging import getLogger


logging.basicConfig(
    format='{asctime:15} {levelname:7} {message}',
    style='{',
    level=logging.DEBUG
)

logging.getLogger('sh').setLevel(logging.WARN)


__all__ = ['getLogger']
