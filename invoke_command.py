#!/usr/bin/env python

import logging
from remote_rs232 import RemoteRs232


def main():
    # TODO argparse
    # BAUD must be 9600 for sending commands
    remote = RemoteRs232('/dev/tty.usbserial-FTE2V28X', log_level=logging.DEBUG, baud_rate=9600)
    #remote.volume_set(8)
    #remote.volume_up()
    #remote.key_volup()
    #remote.set_source('hdmi2')
    remote.power_toggle()
    #remote.key_factory()
    remote.key_3speed()
    #remote.key_dnet()
    remote.close()


if __name__ == '__main__':

    main()
