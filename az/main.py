import argparse

from az.logger import getLogger
from az.config import get_config
from az.router import Router
from az import constants


logger = getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(constants.PACKAGE_NAME)

    parser.add_argument('--config', '-c', default='config.yml',
                        help="Configuration file to use")

    return parser.parse_args()


def run():
    logger.debug("Starting az")
    args = parse_args()

    router = Router(get_config(args.config))

    router()
