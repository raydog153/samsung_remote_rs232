# -*- coding: utf-8 -*-

"""Samsung Remote control TV via RS232 connection"""

import logging
from remote_rs232 import RemoteRs232

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s')
stream_handle = logging.StreamHandler()
stream_handle.setLevel(logging.INFO)
stream_handle.setFormatter(formatter)
logger.addHandler(stream_handle)
logging.basicConfig(format='%(asctime)s %(name)s [%(levelname)s] %(message)s', level=logging.INFO)

__title__ = "samsung_remote_rs232"
__version__ = "0.0.0a"
__url__ = "https://github.com/raydog153/samsung_remote_rs232"
__author__ = "Ray Boutotte"
__author_email__ = "ray.boutotte@gmail.com"
__license__ = "MIT"


def main(device_name='/dev/ttyUSB0', log_level=logging.INFO):
    yield RemoteRs232(device_name, log_level)